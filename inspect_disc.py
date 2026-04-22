"""Inspect an optical disc and show what the fingerprint covers.

Usage:
    python inspect_disc.py <path> [--no-fingerprint] [--json]

<path> may be either a mounted disc directory (e.g. /media/user/DISC) or an
ISO image file. ISO images are loop-mounted read-only via udisksctl for the
duration of the inspection and cleaned up afterwards.

Shows disc type, files included in the fingerprint (in spec order, with sizes),
and files present but excluded by the spec (with the reason). Useful for
verifying spec compliance on real discs and for building an evaluation corpus.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from matrix256 import (
    SelectionEntry,
    detect_disc_type,
    hash_files,
    select_bluray_files,
    select_dvd_files,
)

DVD_EXCLUSION_REASONS = {
    ".BUP": "backup file — duplicates primary IFO bytes",
    ".VOB": "video payload — structural hash only",
}

BLURAY_EXCLUSION_DIRS = {
    "STREAM": "video payload (M2TS) — structural hash only",
    "AUXDATA": "auxiliary data — excluded by spec",
    "BDJO": "BD-J objects — excluded by spec",
    "JAR": "BD-J jars — excluded by spec",
    "META": "metadata directory — excluded by spec",
    "BACKUP": "backup directory — duplicates primary files",
}


class IsoMountError(RuntimeError):
    pass


def _udisks(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["udisksctl", *args, "--no-user-interaction"],
        capture_output=True, text=True, check=False,
    )


def _wait_for_mount(device: str, timeout: float) -> str | None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        out = subprocess.run(
            ["lsblk", "-nro", "MOUNTPOINT", device],
            capture_output=True, text=True, check=False,
        )
        mp = out.stdout.strip().splitlines()
        if mp and mp[0]:
            return mp[0]
        time.sleep(0.1)
    return None


_MOUNT_RE = re.compile(r"(?:[Mm]ounted .* at|already mounted at) [`']?(.+?)[`'.]?\s*$", re.M)


def _mount_loop_device(device: str) -> str:
    out = _udisks("mount", "-b", device)
    text = (out.stdout or "") + "\n" + (out.stderr or "")
    if out.returncode != 0 and "already mounted" not in text:
        raise IsoMountError(text.strip() or f"udisksctl mount -b {device} failed")
    m = _MOUNT_RE.search(text)
    if not m:
        raise IsoMountError(f"could not parse mount point for {device}: {text.strip()!r}")
    return m.group(1).strip()


@contextlib.contextmanager
def loop_mount_iso(iso_path: Path):
    """Loop-mount an ISO read-only via udisksctl; unmount and detach on exit."""
    if shutil.which("udisksctl") is None:
        raise IsoMountError(
            "udisksctl not found — install udisks2 or mount the ISO manually and pass the mount point."
        )
    setup = _udisks("loop-setup", "-r", "-f", str(iso_path))
    if setup.returncode != 0:
        raise IsoMountError(f"loop-setup failed: {(setup.stderr or setup.stdout).strip()}")
    m = re.search(r"as (/dev/loop\d+)", setup.stdout)
    if not m:
        raise IsoMountError(f"could not parse loop device from: {setup.stdout!r}")
    device = m.group(1)
    try:
        mount_point = _wait_for_mount(device, timeout=5.0) or _mount_loop_device(device)
        yield Path(mount_point)
    finally:
        _udisks("unmount", "-b", device)
        _udisks("loop-delete", "-b", device)


def _fmt_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n/1024:.1f} KB"
    if n < 1024 * 1024 * 1024:
        return f"{n/1024/1024:.1f} MB"
    return f"{n/1024/1024/1024:.2f} GB"


def find_dvd_exclusions(mountpoint: Path) -> list[tuple[str, int, str]]:
    video_ts = mountpoint / "VIDEO_TS"
    if not video_ts.is_dir():
        return []
    excluded: list[tuple[str, int, str]] = []
    for p in sorted(video_ts.iterdir()):
        if not p.is_file():
            continue
        suffix = p.suffix.upper()
        if suffix == ".IFO" and (p.name == "VIDEO_TS.IFO" or p.name.endswith("_0.IFO")):
            continue
        reason = DVD_EXCLUSION_REASONS.get(suffix, "not part of fingerprint input set")
        excluded.append((f"VIDEO_TS/{p.name}", p.stat().st_size, reason))
    return excluded


def find_bluray_exclusions(mountpoint: Path) -> list[tuple[str, int, str]]:
    bdmv = mountpoint / "BDMV"
    if not bdmv.is_dir():
        return []
    excluded: list[tuple[str, int, str]] = []
    for child in sorted(bdmv.iterdir()):
        if child.is_dir() and child.name in BLURAY_EXCLUSION_DIRS:
            total = sum(p.stat().st_size for p in child.rglob("*") if p.is_file())
            excluded.append((f"BDMV/{child.name}/", total, BLURAY_EXCLUSION_DIRS[child.name]))
    return excluded


def render_text(
    source: Path,
    mount: Path,
    disc_type: str,
    included: list[SelectionEntry],
    excluded: list[tuple[str, int, str]],
    fingerprint: str | None,
) -> str:
    lines: list[str] = []
    lines.append(f"Source:    {source}")
    if mount != source:
        lines.append(f"Mount:     {mount}")
    lines.append(f"Disc type: {disc_type}")
    lines.append("")

    if not included:
        lines.append("No fingerprint input files found.")
        if disc_type == "unknown":
            lines.append("This path does not contain a VIDEO_TS or BDMV directory.")
            lines.append("Audio CDs are not inspectable from a filesystem path; use a MusicBrainz Disc ID tool (libdiscid / python-discid).")
        return "\n".join(lines)

    total = sum(e.path.stat().st_size for e in included)
    lines.append(f"Files included in fingerprint ({len(included)} files, {_fmt_size(total)}):")
    width = max(len(e.relative) for e in included)
    for i, e in enumerate(included, 1):
        size = e.path.stat().st_size
        lines.append(f"  {i:>3}. {e.relative:<{width}}  {_fmt_size(size):>10}")
    lines.append("")

    if excluded:
        lines.append(f"Files present but excluded by spec ({len(excluded)}):")
        ex_width = max(len(name) for name, _, _ in excluded)
        for name, size, reason in excluded:
            lines.append(f"       {name:<{ex_width}}  {_fmt_size(size):>10}  ({reason})")
        lines.append("")

    if fingerprint is not None:
        lines.append(f"Fingerprint (SHA-256): {fingerprint}")
    else:
        lines.append("Fingerprint: not computed (--no-fingerprint)")
    return "\n".join(lines)


def build_report(source: Path, mount: Path, compute: bool) -> dict:
    disc_type = detect_disc_type(mount)
    if disc_type == "dvd":
        included = select_dvd_files(mount)
        excluded = find_dvd_exclusions(mount)
    elif disc_type == "bluray":
        included = select_bluray_files(mount)
        excluded = find_bluray_exclusions(mount)
    else:
        included = []
        excluded = []

    fingerprint = hash_files(included) if compute and included else None

    return {
        "source": str(source),
        "mount": str(mount),
        "disc_type": disc_type,
        "included": [
            {"path": e.relative, "size": e.path.stat().st_size} for e in included
        ],
        "excluded": [
            {"path": name, "size": size, "reason": reason}
            for name, size, reason in excluded
        ],
        "fingerprint": fingerprint,
    }


def _inspect(source: Path, mount: Path, *, compute: bool, as_json: bool) -> None:
    report = build_report(source, mount, compute=compute)
    if as_json:
        print(json.dumps(report, indent=2))
        return
    included = [
        SelectionEntry(mount / entry["path"], entry["path"])
        for entry in report["included"]
    ]
    excluded = [(e["path"], e["size"], e["reason"]) for e in report["excluded"]]
    print(render_text(source, mount, report["disc_type"], included, excluded, report["fingerprint"]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect what the disc fingerprint covers on a mounted optical disc or ISO image.")
    parser.add_argument("path", type=Path, help="Mounted disc directory (e.g. /media/user/DISC) or ISO file (.iso)")
    parser.add_argument("--no-fingerprint", action="store_true", help="Skip SHA-256 computation (selection only)")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON report instead of text")
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"error: {args.path} does not exist", file=sys.stderr)
        return 2

    compute = not args.no_fingerprint

    if args.path.is_dir():
        _inspect(args.path, args.path, compute=compute, as_json=args.json)
        return 0
    if args.path.is_file():
        try:
            with loop_mount_iso(args.path) as mount:
                _inspect(args.path, mount, compute=compute, as_json=args.json)
        except IsoMountError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        return 0
    print(f"error: {args.path} is neither a directory nor a regular file", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
