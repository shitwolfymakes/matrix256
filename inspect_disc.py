"""Inspect an optical disc mount point and show what the fingerprint covers.

Usage:
    python inspect_disc.py <mountpoint> [--no-fingerprint] [--json]

Shows disc type, files included in the fingerprint (in spec order, with sizes),
and files present but excluded by the spec (with the reason). Useful for
verifying spec compliance on real discs and for building an evaluation corpus.
"""

from __future__ import annotations

import argparse
import json
import sys
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
    mountpoint: Path,
    disc_type: str,
    included: list[SelectionEntry],
    excluded: list[tuple[str, int, str]],
    fingerprint: str | None,
) -> str:
    lines: list[str] = []
    lines.append(f"Mount:     {mountpoint}")
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


def build_report(mountpoint: Path, compute: bool) -> dict:
    disc_type = detect_disc_type(mountpoint)
    if disc_type == "dvd":
        included = select_dvd_files(mountpoint)
        excluded = find_dvd_exclusions(mountpoint)
    elif disc_type == "bluray":
        included = select_bluray_files(mountpoint)
        excluded = find_bluray_exclusions(mountpoint)
    else:
        included = []
        excluded = []

    fingerprint = hash_files(included) if compute and included else None

    return {
        "mountpoint": str(mountpoint),
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect what the disc fingerprint covers on a mounted optical disc.")
    parser.add_argument("mountpoint", type=Path, help="Path to the mounted disc (e.g. /mnt/dvd, /media/user/BDMV_DISC)")
    parser.add_argument("--no-fingerprint", action="store_true", help="Skip SHA-256 computation (selection only)")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON report instead of text")
    args = parser.parse_args(argv)

    if not args.mountpoint.exists():
        print(f"error: {args.mountpoint} does not exist", file=sys.stderr)
        return 2
    if not args.mountpoint.is_dir():
        print(f"error: {args.mountpoint} is not a directory", file=sys.stderr)
        return 2

    report = build_report(args.mountpoint, compute=not args.no_fingerprint)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        disc_type = report["disc_type"]
        included = [
            SelectionEntry(args.mountpoint / entry["path"], entry["path"])
            for entry in report["included"]
        ]
        excluded = [(e["path"], e["size"], e["reason"]) for e in report["excluded"]]
        print(render_text(args.mountpoint, disc_type, included, excluded, report["fingerprint"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
