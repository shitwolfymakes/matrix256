"""Inspect an optical disc and show what the fingerprint covers.

Usage:
    python inspect_disc.py <path> [--no-fingerprint] [--no-metadata] [--json]

<path> may be a mounted disc directory (e.g. /media/user/DISC), an ISO image
file, or a block device (e.g. /dev/sr0). ISO images are loop-mounted read-only
via udisksctl; block devices are mounted via udisksctl if not already mounted
by the desktop. Either way, anything the script mounted is unmounted on exit.

Shows disc type, files included in the fingerprint (in spec order, with sizes),
files present but excluded by the spec (with the reason), and a MakeMKV-style
metadata summary (titles, durations, chapters, streams). Metadata extraction
uses lsdvd for DVDs and libbluray's bd_info/bd_list_titles for Blu-rays;
install `lsdvd` and `libbluray-bin` to enable. Useful for verifying spec
compliance on real discs and for building an evaluation corpus.
"""

from __future__ import annotations

import argparse
import ast
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


def _loop_is_attached(device: str) -> bool:
    """True if the loop device still has a backing file. udisks2 sets
    auto-clear on loops it creates, so /sys/block/loopN/loop disappears
    when the kernel detaches the device."""
    return Path(f"/sys/block/{device.rsplit('/', 1)[-1]}/loop").exists()


def _udisks_unmount(device: str) -> subprocess.CompletedProcess[str]:
    """udisksctl unmount -b <device>, retrying briefly on transient busy so
    we don't give up just because a subprocess hasn't fully released yet."""
    result = _udisks("unmount", "-b", device)
    for _ in range(4):
        text = (result.stdout or "") + (result.stderr or "")
        if result.returncode == 0 or "ot mounted" in text:
            return result
        time.sleep(0.2)
        result = _udisks("unmount", "-b", device)
    return result


def _cleanup_loop(device: str) -> None:
    """Unmount the ISO and let the kernel auto-clear the loop. Some udisks2
    polkit configurations require admin auth for loop-delete even on loops
    the same session created, which --no-user-interaction can't satisfy; but
    auto-clear makes loop-delete unnecessary in the common case. We only fall
    back to an explicit loop-delete if auto-clear hasn't fired."""
    result = _udisks_unmount(device)
    text = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0 and "ot mounted" not in text:
        print(f"warning: failed to unmount {device}: {(result.stderr or result.stdout).strip()}", file=sys.stderr)
        return
    for _ in range(20):
        if not _loop_is_attached(device):
            return
        time.sleep(0.1)
    delete = _udisks("loop-delete", "-b", device)
    if delete.returncode != 0 and _loop_is_attached(device):
        print(f"warning: failed to detach {device}: {(delete.stderr or delete.stdout).strip()}", file=sys.stderr)


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
        _cleanup_loop(device)


@contextlib.contextmanager
def mount_block_device(device: Path):
    """Mount a block device (e.g. /dev/sr0) read-only via udisksctl if not
    already mounted, yielding the mount point. If the disc was already mounted
    by the desktop we leave that mount alone on exit; we only unmount what
    this function mounted."""
    if shutil.which("udisksctl") is None:
        raise IsoMountError(
            "udisksctl not found — install udisks2 or mount the disc manually and pass the mount point."
        )
    device_str = str(device)
    existing = _wait_for_mount(device_str, timeout=0.1)
    if existing:
        yield Path(existing)
        return
    mount_point = _mount_loop_device(device_str)
    try:
        yield Path(mount_point)
    finally:
        result = _udisks_unmount(device_str)
        text = (result.stdout or "") + (result.stderr or "")
        if result.returncode != 0 and "ot mounted" not in text:
            print(f"warning: failed to unmount {device_str}: {(result.stderr or result.stdout).strip()}", file=sys.stderr)


def _extract_dvd_metadata(mount: Path) -> dict | None:
    """Parse DVD title/chapter/stream metadata via `lsdvd -x -Oy`.

    Returns None if lsdvd is not installed or fails. `-Oy` emits a Python-literal
    dict prefixed with `lsdvd = `; we slice from the opening brace and
    ast.literal_eval the rest. Some libdvdread warnings land on stdout, so we
    tolerate any preamble before that marker.
    """
    if shutil.which("lsdvd") is None:
        return None
    out = subprocess.run(
        ["lsdvd", "-x", "-Oy", str(mount)],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0 or "lsdvd = {" not in out.stdout:
        return None
    raw = out.stdout[out.stdout.index("lsdvd = {") + len("lsdvd = "):]
    try:
        parsed = ast.literal_eval(raw)
    except (SyntaxError, ValueError):
        return None

    titles = []
    for t in parsed.get("track", []):
        audio = [
            {
                "lang": a.get("langcode") or a.get("language"),
                "format": a.get("format"),
                "channels": a.get("channels"),
            }
            for a in t.get("audio", [])
        ]
        subs = [
            {"lang": s.get("langcode") or s.get("language")}
            for s in t.get("subp", [])
        ]
        titles.append({
            "index": t.get("ix"),
            "length_seconds": t.get("length"),
            "chapters": len(t.get("chapter", [])),
            "format": t.get("format"),
            "aspect": t.get("aspect"),
            "resolution": f"{t.get('width')}x{t.get('height')}" if t.get("width") else None,
            "audio": audio,
            "subtitles": subs,
        })
    return {
        "tool": "lsdvd",
        "disc_title": parsed.get("title"),
        "provider_id": parsed.get("provider_id"),
        "longest_track": parsed.get("longest_track"),
        "titles": titles,
    }


_BD_TITLE_RE = re.compile(
    r"index:\s*(?P<index>\d+)\s+"
    r"duration:\s*(?P<duration>\d\d:\d\d:\d\d)\s+"
    r"chapters:\s*(?P<chapters>\d+)\s+"
    r"angles:\s*(?P<angles>\d+)\s+"
    r"clips:\s*(?P<clips>\d+)\s+"
    r"\(playlist:\s*(?P<playlist>[^)]+)\)\s+"
    r"V:(?P<v>\d+)\s+A:(?P<a>\d+)\s+PG:(?P<pg>\d+)\s+IG:(?P<ig>\d+)\s+SV:(?P<sv>\d+)\s+SA:(?P<sa>\d+)"
)


def _extract_bluray_metadata(mount: Path) -> dict | None:
    """Parse BD disc and per-title metadata via bd_info + bd_list_titles."""
    if shutil.which("bd_info") is None or shutil.which("bd_list_titles") is None:
        return None

    info = subprocess.run(
        ["bd_info", str(mount)],
        capture_output=True, text=True, check=False,
    )
    if info.returncode != 0:
        return None
    disc: dict = {"tool": "libbluray"}
    toc: list[dict] = []
    in_toc = False
    for line in info.stdout.splitlines():
        if ":" in line and not line.startswith("\t"):
            key, _, value = line.partition(":")
            k = key.strip()
            v = value.strip()
            if k == "HDMV titles":
                disc["hdmv_titles"] = int(v)
            elif k == "BD-J titles":
                disc["bdj_titles"] = int(v)
            elif k == "UNSUPPORTED titles":
                disc["unsupported_titles"] = int(v)
            elif k == "AACS detected":
                disc["aacs"] = (v == "yes")
            elif k == "BD+ detected":
                disc["bdplus"] = (v == "yes")
            elif k == "BD-J detected":
                disc["bdj"] = (v == "yes")
            elif k == "Disc name":
                disc["disc_name"] = v
            elif k == "Disc ID":
                disc["disc_id"] = v
            in_toc = k == "TOC count"
        elif in_toc and line.startswith("\tTitle "):
            m = re.match(r"\tTitle (\d+): (.+?)\s*$", line)
            if m:
                toc.append({"title": int(m.group(1)), "name": m.group(2)})
    if toc:
        disc["toc"] = toc

    titles_out = subprocess.run(
        ["bd_list_titles", "-l", str(mount)],
        capture_output=True, text=True, check=False,
    )
    titles: list[dict] = []
    main_title = None
    if titles_out.returncode == 0:
        lines = titles_out.stdout.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            m = re.match(r"Main title:\s*(\d+)", line)
            if m:
                main_title = int(m.group(1))
            tm = _BD_TITLE_RE.search(line)
            if tm:
                entry = {
                    "index": int(tm["index"]),
                    "duration": tm["duration"],
                    "chapters": int(tm["chapters"]),
                    "angles": int(tm["angles"]),
                    "clips": int(tm["clips"]),
                    "playlist": tm["playlist"],
                    "streams": {
                        "video": int(tm["v"]),
                        "audio": int(tm["a"]),
                        "subs": int(tm["pg"]),
                        "interactive": int(tm["ig"]),
                        "secondary_video": int(tm["sv"]),
                        "secondary_audio": int(tm["sa"]),
                    },
                }
                if i + 1 < len(lines) and lines[i + 1].startswith("\tAUD:"):
                    entry["audio_langs"] = lines[i + 1].strip()[5:].split()
                    i += 1
                titles.append(entry)
            i += 1
    if main_title is not None:
        disc["main_title_index"] = main_title
    disc["titles"] = titles
    return disc


def _extract_metadata(disc_type: str, mount: Path) -> dict | None:
    if disc_type == "dvd":
        return _extract_dvd_metadata(mount)
    if disc_type == "bluray":
        return _extract_bluray_metadata(mount)
    return None


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


def _fmt_hms(seconds: float) -> str:
    total = int(round(seconds))
    h, r = divmod(total, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _summarize_dvd_audio(audio: list[dict]) -> str:
    if not audio:
        return "—"
    from collections import Counter
    keys = [f"{a.get('lang') or '?'}/{a.get('format') or '?'}/{a.get('channels') or '?'}ch" for a in audio]
    counts = Counter(keys)
    return ", ".join(f"{k}×{n}" if n > 1 else k for k, n in counts.items())


def _summarize_dvd_subs(subs: list[dict]) -> str:
    if not subs:
        return "—"
    from collections import Counter
    langs = Counter(s.get("lang") or "?" for s in subs)
    return ", ".join(f"{k}×{n}" if n > 1 else k for k, n in langs.items())


def render_metadata_dvd(md: dict) -> list[str]:
    lines = [f"Metadata ({md['tool']}):"]
    if md.get("disc_title") and md["disc_title"] != "unknown":
        lines.append(f"  Disc title:     {md['disc_title']}")
    if md.get("provider_id"):
        lines.append(f"  Provider ID:    {md['provider_id']}")
    if md.get("longest_track"):
        lines.append(f"  Longest track:  #{md['longest_track']}")
    titles = md.get("titles") or []
    if titles:
        lines.append("")
        lines.append(f"  Titles ({len(titles)}):")
        lines.append(f"    {'#':>3}  {'Length':<11}  {'Ch':>3}  {'Res':<9}  {'Audio':<36}  Subs")
        for t in titles:
            length = _fmt_hms(t.get("length_seconds") or 0)
            chapters = t.get("chapters") or 0
            res = t.get("resolution") or "—"
            audio = _summarize_dvd_audio(t.get("audio") or [])
            subs = _summarize_dvd_subs(t.get("subtitles") or [])
            if len(audio) > 36:
                audio = audio[:33] + "..."
            lines.append(f"    {t['index']:>3}  {length:<11}  {chapters:>3}  {res:<9}  {audio:<36}  {subs}")
    return lines


def render_metadata_bluray(md: dict) -> list[str]:
    lines = [f"Metadata ({md['tool']}):"]
    if md.get("disc_name"):
        lines.append(f"  Disc name:      {md['disc_name']}")
    if md.get("disc_id"):
        lines.append(f"  Disc ID:        {md['disc_id']}")
    counts = []
    for k, label in (("hdmv_titles", "HDMV"), ("bdj_titles", "BD-J"), ("unsupported_titles", "unsupported")):
        if k in md:
            counts.append(f"{md[k]} {label}")
    if counts:
        lines.append(f"  Title counts:   {', '.join(counts)}")
    flags = []
    for k, label in (("aacs", "AACS"), ("bdplus", "BD+"), ("bdj", "BD-J")):
        if k in md:
            flags.append(f"{label}={'yes' if md[k] else 'no'}")
    if flags:
        lines.append(f"  Protection:     {', '.join(flags)}")
    if md.get("main_title_index") is not None:
        lines.append(f"  Main title:     #{md['main_title_index']}")
    titles = md.get("titles") or []
    if titles:
        lines.append("")
        lines.append(f"  Titles (≥180s, shown {len(titles)}):")
        lines.append(f"    {'#':>3}  {'Duration':<8}  {'Ch':>3}  {'Playlist':<12}  {'V/A/Sub/IG':<12}  Audio langs")
        for t in titles:
            streams = t.get("streams") or {}
            stream_str = f"{streams.get('video', 0)}/{streams.get('audio', 0)}/{streams.get('subs', 0)}/{streams.get('interactive', 0)}"
            langs = t.get("audio_langs") or []
            langs_str = " ".join(langs) if langs else "—"
            if len(langs_str) > 28:
                langs_str = langs_str[:25] + "..."
            lines.append(f"    {t['index']:>3}  {t['duration']:<8}  {t['chapters']:>3}  {t['playlist']:<12}  {stream_str:<12}  {langs_str}")
    toc = md.get("toc") or []
    if toc:
        lines.append("")
        lines.append(f"  Disc library TOC ({len(toc)}):")
        for entry in toc:
            lines.append(f"    Title {entry['title']}: {entry['name']}")
    return lines


def render_metadata(md: dict | None, disc_type: str) -> list[str]:
    if md is None:
        if disc_type == "dvd":
            return ["Metadata: lsdvd not installed or failed (apt install lsdvd)"]
        if disc_type == "bluray":
            return ["Metadata: libbluray tools not installed or failed (apt install libbluray-bin)"]
        return []
    if disc_type == "dvd":
        return render_metadata_dvd(md)
    if disc_type == "bluray":
        return render_metadata_bluray(md)
    return []


def render_text(
    source: Path,
    mount: Path,
    disc_type: str,
    included: list[SelectionEntry],
    excluded: list[tuple[str, int, str]],
    fingerprint: str | None,
    metadata: dict | None = None,
    show_metadata: bool = True,
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

    if show_metadata:
        md_lines = render_metadata(metadata, disc_type)
        if md_lines:
            lines.append("")
            lines.extend(md_lines)
    return "\n".join(lines)


def build_report(source: Path, mount: Path, compute: bool, include_metadata: bool = True) -> dict:
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
    metadata = _extract_metadata(disc_type, mount) if include_metadata else None

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
        "metadata": metadata,
    }


def _inspect(source: Path, mount: Path, *, compute: bool, metadata: bool, as_json: bool) -> None:
    report = build_report(source, mount, compute=compute, include_metadata=metadata)
    if as_json:
        print(json.dumps(report, indent=2))
        return
    included = [
        SelectionEntry(mount / entry["path"], entry["path"])
        for entry in report["included"]
    ]
    excluded = [(e["path"], e["size"], e["reason"]) for e in report["excluded"]]
    print(render_text(
        source, mount, report["disc_type"], included, excluded,
        report["fingerprint"], report.get("metadata"),
        show_metadata=metadata,
    ))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect what the disc fingerprint covers on a mounted optical disc or ISO image.")
    parser.add_argument("path", type=Path, help="Mounted disc directory (e.g. /media/user/DISC), ISO file (.iso), or block device (e.g. /dev/sr0)")
    parser.add_argument("--no-fingerprint", action="store_true", help="Skip SHA-256 computation (selection only)")
    parser.add_argument("--no-metadata", action="store_true", help="Skip title/stream metadata extraction (lsdvd / bd_info)")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON report instead of text")
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"error: {args.path} does not exist", file=sys.stderr)
        return 2

    compute = not args.no_fingerprint
    metadata = not args.no_metadata

    if args.path.is_dir():
        _inspect(args.path, args.path, compute=compute, metadata=metadata, as_json=args.json)
        return 0
    if args.path.is_block_device():
        try:
            with mount_block_device(args.path) as mount:
                _inspect(args.path, mount, compute=compute, metadata=metadata, as_json=args.json)
        except IsoMountError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        return 0
    if args.path.is_file():
        try:
            with loop_mount_iso(args.path) as mount:
                _inspect(args.path, mount, compute=compute, metadata=metadata, as_json=args.json)
        except IsoMountError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        return 0
    print(f"error: {args.path} is not a directory, block device, or regular file", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
