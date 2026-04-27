"""Inspect an optical disc and compute its matrix256v1 fingerprint.

Usage:
    python inspect_disc.py <path> [--no-fingerprint] [--no-metadata] [--json]

<path> may be a mounted disc directory (e.g. /media/user/DISC), an ISO image
file, or a block device (e.g. /dev/sr0). ISO images are loop-mounted read-only
via udisksctl; block devices are mounted via udisksctl if not already mounted
by the desktop. Either way, anything the script mounted is unmounted on exit.

Computes the matrix256v1 digest (filesystem-walk hash over (path, size)
records) and reports the IMPLEMENTERS.md §5 submission view: source kind,
filesystem driver, mount options, and reader info. Also surfaces a
MakeMKV-style metadata summary (titles, durations, chapters, streams) when
the disc carries DVD-Video or BDMV structure. Metadata extraction uses
lsdvd for DVDs and libbluray's bd_info/bd_list_titles for Blu-rays; install
`lsdvd` and `libbluray-bin` to enable. Useful for verifying spec compliance
on real discs and for building an evaluation corpus.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import csv
import json
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from xml.dom import minidom
from xml.parsers.expat import ExpatError

from matrix256 import v1


def detect_disc_type(mountpoint: Path) -> str:
    """Classify the mount as DVD-Video, Blu-ray, or unknown — used only to
    route the metadata-extraction step (lsdvd vs bd_info). The matrix256v1
    fingerprint walks the whole filesystem regardless and does not depend
    on this classification."""
    if (mountpoint / "VIDEO_TS").is_dir():
        return "dvd"
    if (mountpoint / "BDMV").is_dir():
        return "bluray"
    return "unknown"


class IsoMountError(RuntimeError):
    pass


def _udisks(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["udisksctl", *args, "--no-user-interaction"],
        capture_output=True, text=True, check=False,
    )


_HEX_ESCAPE_RE = re.compile(r"\\x([0-9a-fA-F]{2})")


def _unescape_mountpoint(s: str) -> str:
    """Un-escape \\xHH sequences that `lsblk -nro MOUNTPOINT` and `udisksctl
    mount` apply to paths containing spaces or other shell-unsafe characters
    (e.g. `/media/u/Disc\\x20Name` → `/media/u/Disc Name`). Both tools use the
    same encoding; without this the escaped string gets passed back through
    as a literal path and downstream `VIDEO_TS`/`BDMV` detection fails."""
    return _HEX_ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), s)


def _wait_for_mount(device: str, timeout: float) -> str | None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        out = subprocess.run(
            ["lsblk", "-nro", "MOUNTPOINT", device],
            capture_output=True, text=True, check=False,
        )
        mp = out.stdout.strip().splitlines()
        if mp and mp[0]:
            return _unescape_mountpoint(mp[0])
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
    return _unescape_mountpoint(m.group(1).strip())


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


def _aacs_on_non_physical_source(source: Path, mount: Path) -> bool:
    """libbluray (`bd_info`, `bd_list_titles`) and `makemkvcon` need an
    optical drive to negotiate the AACS Drive Authentication handshake and
    extract the disc's Volume ID from the BD-ROM Mark — a pre-recorded
    zone that lives outside the user-data filesystem and is only readable
    via SCSI MMC commands. ISOs (loop-mounted regular files) have no MMC
    channel, and `dd` can't have captured the BD-ROM Mark in the first
    place, so libaacs can't complete the handshake and instead stalls
    indefinitely after warning that no `KEYDB.cfg` was found. When we
    detect this combination — a non-block-device source with an `AACS/`
    directory — we skip those tools rather than timing them out."""
    if source.is_block_device():
        return False
    return (mount / "AACS").is_dir()


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
        encoding="utf-8", errors="replace",
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


def _extract_bluray_metadata(source: Path, mount: Path) -> dict | None:
    """Parse BD disc and per-title metadata via bd_info + bd_list_titles."""
    if shutil.which("bd_info") is None or shutil.which("bd_list_titles") is None:
        return None
    if _aacs_on_non_physical_source(source, mount):
        print(
            "warning: skipping libbluray on AACS-structured non-physical source "
            "(no MMC channel for the AACS handshake)",
            file=sys.stderr,
        )
        return None

    info = subprocess.run(
        ["bd_info", str(mount)],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
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
        encoding="utf-8", errors="replace",
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


def _extract_metadata(disc_type: str, source: Path, mount: Path) -> dict | None:
    if disc_type == "dvd":
        return _extract_dvd_metadata(mount)
    if disc_type == "bluray":
        return _extract_bluray_metadata(source, mount)
    return None


def _parse_makemkv_robot(output: str) -> dict:
    """Parse `makemkvcon -r info` output into disc-level and per-title attribute maps.

    Robot-mode lines are CSV-ish: `PREFIX:<csv fields>`. We keep CINFO
    (disc-level) and TINFO (per-title) rows and ignore everything else; MSG
    and SINFO lines are not needed for the title summary we surface.
    """
    disc: dict[int, str] = {}
    titles: dict[int, dict[int, str]] = {}
    for raw in output.splitlines():
        if ":" not in raw:
            continue
        prefix, _, rest = raw.partition(":")
        if prefix not in ("CINFO", "TINFO"):
            continue
        try:
            fields = next(csv.reader([rest]))
        except (csv.Error, StopIteration):
            continue
        if prefix == "CINFO" and len(fields) >= 3:
            try:
                attr_id = int(fields[0])
            except ValueError:
                continue
            disc[attr_id] = fields[2]
        elif prefix == "TINFO" and len(fields) >= 4:
            try:
                title_idx = int(fields[0])
                attr_id = int(fields[1])
            except ValueError:
                continue
            titles.setdefault(title_idx, {})[attr_id] = fields[3]
    return {"disc": disc, "titles": titles}


def _extract_makemkv_metadata(source: Path, mount: Path) -> dict | None:
    """Run `makemkvcon -r info` against the disc and return a title summary.

    Complements lsdvd / bd_info by surfacing MakeMKV's tighter title selection
    and its main-title heuristic (useful on decoy-heavy discs). Source spec
    depends on what the user pointed at: `dev:<device>` for block devices
    (MakeMKV drives CSS/AACS key handshakes directly), `iso:<path>` for ISO
    files, and `file:<mount>` for already-mounted directories. `file:<mount>`
    can't read CSS-protected VOBs because the kernel returns EIO — the dev/iso
    paths let MakeMKV decrypt in-process.
    Returns None if makemkvcon is not installed or the invocation fails.
    """
    if shutil.which("makemkvcon") is None:
        return None
    if _aacs_on_non_physical_source(source, mount):
        print(
            "warning: skipping makemkvcon on AACS-structured non-physical source "
            "(no MMC channel for the AACS handshake)",
            file=sys.stderr,
        )
        return None
    if source.is_block_device():
        spec = f"dev:{source}"
    elif source.is_file():
        spec = f"iso:{source}"
    else:
        spec = f"file:{mount}"
    out = subprocess.run(
        ["makemkvcon", "-r", "info", spec],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
    )
    if out.returncode != 0:
        return None
    raw = _parse_makemkv_robot(out.stdout)
    if not raw["titles"]:
        return None
    info: dict = {"tool": "makemkv"}
    disc = raw["disc"]
    if 1 in disc:
        info["disc_kind"] = disc[1]
    if 2 in disc:
        info["disc_name"] = disc[2]
    if 32 in disc:
        info["volume_name"] = disc[32]
    titles_out: list[dict] = []
    for idx in sorted(raw["titles"].keys()):
        t = raw["titles"][idx]
        # attr 16 (SourceFileName) is populated for BD playlists (e.g. "00800.mpls")
        # but not for DVDs; fall back to attr 24 (OriginalTitleId), which on DVDs
        # is the original title number used by the disc author ("01" → "T01").
        source_file = t.get(16)
        if not source_file and 24 in t:
            source_file = f"T{t[24]}"
        titles_out.append({
            "index": idx,
            "duration": t.get(9),
            "chapters": int(t[8]) if 8 in t and t[8].isdigit() else None,
            "size": t.get(10),
            "size_bytes": int(t[11]) if 11 in t and t[11].isdigit() else None,
            "source_file": source_file,
            "segments_count": int(t[25]) if 25 in t and t[25].isdigit() else None,
            "output_file": t.get(27),
            "selected": 27 in t,
        })
    info["titles"] = titles_out
    selected = [t for t in titles_out if t["selected"] and t.get("duration")]
    if selected:
        info["main_title_index"] = max(selected, key=lambda t: _hms_to_seconds(t["duration"]))["index"]
    return info


def _hms_to_seconds(s: str) -> int:
    """Parse an HH:MM:SS or MM:SS MakeMKV duration into total seconds; 0 on parse failure."""
    try:
        parts = [int(p) for p in s.split(":")]
    except ValueError:
        return 0
    if len(parts) == 3:
        h, m, sec = parts
    elif len(parts) == 2:
        h = 0
        m, sec = parts
    else:
        return 0
    return h * 3600 + m * 60 + sec


def _read_disc_library_xml(disc_type: str, mount: Path) -> dict | None:
    """Read BDMV/META/DL/bdmt_eng.xml for Blu-ray discs.

    Returns None for non-BD discs. For BD, always returns a dict with `found`
    so the caller can report the absence. Independent of libbluray tooling —
    this is just a file read.
    """
    if disc_type != "bluray":
        return None
    rel = "BDMV/META/DL/bdmt_eng.xml"
    path = mount / "BDMV" / "META" / "DL" / "bdmt_eng.xml"
    if not path.is_file():
        return {"path": rel, "found": False, "content": None}
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"path": rel, "found": True, "content": None, "error": str(e)}
    return {"path": rel, "found": True, "content": content}


def _detect_source_kind(path: Path) -> str:
    """Classify the original `path` argument per IMPLEMENTERS.md §5: physical
    disc (block device), ISO image (regular file), or filesystem (already-
    mounted directory whose underlying source we can't infer). Surfacing this
    matters for lookup-service submissions, where a single physical pressing
    can produce different digests through different filesystem views."""
    if path.is_block_device():
        return "physical_disc"
    if path.is_file():
        return "iso_image"
    if path.is_dir():
        return "filesystem"
    return "unknown"


def _detect_filesystem_view(mount: Path) -> dict:
    """Query findmnt for the filesystem driver and mount options at `mount`.

    `findmnt -T <path>` walks up to the closest enclosing mountpoint, so this
    works whether `mount` is itself the mount target or a subdirectory.
    Returns an empty dict if findmnt is missing or doesn't report a mount.
    """
    if shutil.which("findmnt") is None:
        return {}
    out = subprocess.run(
        ["findmnt", "-J", "-T", str(mount), "-o", "FSTYPE,OPTIONS,SOURCE"],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0 or not out.stdout.strip():
        return {}
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        return {}
    fs_list = data.get("filesystems") or []
    if not fs_list:
        return {}
    fs = fs_list[0]
    view: dict = {}
    if fs.get("fstype"):
        view["filesystem"] = fs["fstype"]
    if fs.get("options"):
        view["mount_options"] = fs["options"]
    if fs.get("source"):
        view["mount_device"] = fs["source"]
    return view


def _reader_info() -> dict:
    """Capture the OS and Python version used to enumerate the filesystem.

    Per IMPLEMENTERS.md §5 these are optional audit fields, useful when a
    digest needs to be reconciled against another implementation that picked
    a different default view (e.g. ISO 9660 vs UDF on a bridge disc).
    """
    return {
        "tool": "inspect_disc.py",
        "python": platform.python_version(),
        "os": f"{platform.system()} {platform.release()}".strip(),
    }


def _build_submission_view(source: Path, mount: Path) -> dict:
    view = {"source_kind": _detect_source_kind(source)}
    view.update(_detect_filesystem_view(mount))
    view["reader"] = _reader_info()
    return view


def _fmt_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n/1024:.1f} KB"
    if n < 1024 * 1024 * 1024:
        return f"{n/1024/1024:.1f} MB"
    return f"{n/1024/1024/1024:.2f} GB"


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


def render_metadata_makemkv(md: dict | None) -> list[str]:
    if md is None:
        if shutil.which("makemkvcon") is None:
            return ["Metadata (makemkv): makemkvcon not installed"]
        return ["Metadata (makemkv): makemkvcon failed or returned no titles"]
    lines = [f"Metadata ({md['tool']}):"]
    if md.get("disc_name"):
        lines.append(f"  Disc name:      {md['disc_name']}")
    if md.get("disc_kind"):
        lines.append(f"  Disc kind:      {md['disc_kind']}")
    if md.get("volume_name"):
        lines.append(f"  Volume:         {md['volume_name']}")
    if md.get("main_title_index") is not None:
        lines.append(f"  Main title:     #{md['main_title_index']}")
    titles = md.get("titles") or []
    if titles:
        selected = sum(1 for t in titles if t.get("selected"))
        lines.append("")
        lines.append(f"  Titles ({len(titles)}, {selected} selected):")
        lines.append(f"    {'#':>3}  {'Duration':<10}  {'Ch':>3}  {'Source':<14}  {'Segs':>4}  {'Size':>10}  Sel")
        for t in titles:
            duration = t.get("duration") or "—"
            chapters = t.get("chapters")
            chapters_str = str(chapters) if chapters is not None else "—"
            source = t.get("source_file") or "—"
            segs = t.get("segments_count")
            segs_str = str(segs) if segs is not None else "—"
            size = t.get("size") or "—"
            mark = "✓" if t.get("selected") else " "
            lines.append(f"    {t['index']:>3}  {duration:<10}  {chapters_str:>3}  {source:<14}  {segs_str:>4}  {size:>10}  {mark}")
    return lines


def _pretty_xml(content: str) -> str:
    """Indent XML for human reading; fall back to the raw content on parse error."""
    try:
        dom = minidom.parseString(content)
    except (ExpatError, ValueError):
        return content.rstrip()
    pretty = dom.toprettyxml(indent="  ")
    return "\n".join(line for line in pretty.splitlines() if line.strip())


def render_disc_library_xml(dlx: dict | None) -> list[str]:
    if dlx is None:
        return []
    if not dlx.get("found"):
        return [f"Disc library XML ({dlx['path']}): not found"]
    header = f"Disc library XML ({dlx['path']}):"
    if dlx.get("content") is None:
        err = dlx.get("error") or "could not read file"
        return [f"{header} {err}"]
    return [header, _pretty_xml(dlx["content"])]


def render_submission(view: dict) -> list[str]:
    """Render IMPLEMENTERS.md §5 submission fields for the digest's filesystem
    view. Surfaced in every report so users can record it now and forward it
    to a lookup service later."""
    if not view:
        return []
    lines = ["Submission metadata (filesystem view):"]
    lines.append(f"  Source kind:    {view.get('source_kind', 'unknown')}")
    if view.get("filesystem"):
        lines.append(f"  Filesystem:     {view['filesystem']}")
    if view.get("mount_device"):
        lines.append(f"  Mount device:   {view['mount_device']}")
    if view.get("mount_options"):
        lines.append(f"  Mount options:  {view['mount_options']}")
    reader = view.get("reader") or {}
    if reader:
        bits = [b for b in (
            reader.get("tool"),
            f"python {reader['python']}" if reader.get("python") else None,
            reader.get("os"),
        ) if b]
        if bits:
            lines.append(f"  Reader:         {' · '.join(bits)}")
    return lines


def render_text(
    source: Path,
    mount: Path,
    disc_type: str,
    fingerprint: str | None,
    metadata: dict | None = None,
    show_metadata: bool = True,
    disc_library_xml: dict | None = None,
    metadata_makemkv: dict | None = None,
    submission: dict | None = None,
) -> str:
    lines: list[str] = []
    lines.append(f"Source:    {source}")
    if mount != source:
        lines.append(f"Mount:     {mount}")
    lines.append(f"Disc type: {disc_type}")
    lines.append("")

    if fingerprint is None:
        lines.append("Fingerprint: not computed (--no-fingerprint)")
    else:
        lines.append(f"Fingerprint (matrix256v1, SHA-256): {fingerprint}")

    sub_lines = render_submission(submission or {})
    if sub_lines:
        lines.append("")
        lines.extend(sub_lines)

    if show_metadata:
        md_lines = render_metadata(metadata, disc_type)
        if md_lines:
            lines.append("")
            lines.extend(md_lines)
        mm_lines = render_metadata_makemkv(metadata_makemkv)
        if mm_lines:
            lines.append("")
            lines.extend(mm_lines)
        dlx_lines = render_disc_library_xml(disc_library_xml)
        if dlx_lines:
            lines.append("")
            lines.extend(dlx_lines)
    return "\n".join(lines)


def build_report(source: Path, mount: Path, compute: bool, include_metadata: bool = True) -> dict:
    disc_type = detect_disc_type(mount)
    fingerprint = v1.fingerprint(mount) if compute else None
    metadata = _extract_metadata(disc_type, source, mount) if include_metadata else None
    disc_library_xml = _read_disc_library_xml(disc_type, mount) if include_metadata else None
    metadata_makemkv = _extract_makemkv_metadata(source, mount) if include_metadata else None
    submission = _build_submission_view(source, mount)

    return {
        "source": str(source),
        "mount": str(mount),
        "disc_type": disc_type,
        "fingerprint": fingerprint,
        "submission": submission,
        "metadata": metadata,
        "metadata_makemkv": metadata_makemkv,
        "disc_library_xml": disc_library_xml,
    }


def _inspect(source: Path, mount: Path, *, compute: bool, metadata: bool, as_json: bool) -> None:
    report = build_report(source, mount, compute=compute, include_metadata=metadata)
    if as_json:
        print(json.dumps(report, indent=2))
        return
    print(render_text(
        source, mount, report["disc_type"], report["fingerprint"], report.get("metadata"),
        show_metadata=metadata,
        disc_library_xml=report.get("disc_library_xml"),
        metadata_makemkv=report.get("metadata_makemkv"),
        submission=report.get("submission"),
    ))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute the matrix256v1 fingerprint of a mounted optical disc, ISO image, or block device, and surface IMPLEMENTERS.md §5 submission metadata.")
    parser.add_argument("path", type=Path, help="Mounted disc directory (e.g. /media/user/DISC), ISO file (.iso), or block device (e.g. /dev/sr0)")
    parser.add_argument("--no-fingerprint", action="store_true", help="Skip SHA-256 computation; report metadata and submission view only")
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
