"""matrix256 — reference implementation of the optical disc fingerprint.

Factored for reuse. The selection and hashing logic here must stay in lockstep
with the normative reference in README.md. If one changes, the other must too.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SelectionEntry:
    path: Path
    relative: str


def select_dvd_files(mountpoint: Path) -> list[SelectionEntry]:
    video_ts = mountpoint / "VIDEO_TS"
    out: list[SelectionEntry] = []
    vmg = video_ts / "VIDEO_TS.IFO"
    if vmg.is_file():
        out.append(SelectionEntry(vmg, "VIDEO_TS/VIDEO_TS.IFO"))
    for nn in range(1, 100):
        vts = video_ts / f"VTS_{nn:02d}_0.IFO"
        if vts.is_file():
            out.append(SelectionEntry(vts, f"VIDEO_TS/VTS_{nn:02d}_0.IFO"))
    return out


def select_bluray_files(mountpoint: Path) -> list[SelectionEntry]:
    bdmv = mountpoint / "BDMV"
    out: list[SelectionEntry] = []
    for name in ("index.bdmv", "MovieObject.bdmv"):
        p = bdmv / name
        if p.is_file():
            out.append(SelectionEntry(p, f"BDMV/{name}"))
    for p in sorted((bdmv / "PLAYLIST").glob("*.mpls")) if (bdmv / "PLAYLIST").is_dir() else []:
        out.append(SelectionEntry(p, f"BDMV/PLAYLIST/{p.name}"))
    for p in sorted((bdmv / "CLIPINF").glob("*.clpi")) if (bdmv / "CLIPINF").is_dir() else []:
        out.append(SelectionEntry(p, f"BDMV/CLIPINF/{p.name}"))
    return out


def detect_disc_type(mountpoint: Path) -> str:
    if (mountpoint / "VIDEO_TS").is_dir():
        return "dvd"
    if (mountpoint / "BDMV").is_dir():
        return "bluray"
    return "unknown"


def hash_files(entries: list[SelectionEntry]) -> str:
    h = hashlib.sha256()
    for entry in entries:
        with entry.path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 16), b""):
                h.update(chunk)
    return h.hexdigest()


def dvd_fingerprint(mountpoint: Path) -> str:
    return hash_files(select_dvd_files(mountpoint))


def bluray_fingerprint(mountpoint: Path) -> str:
    return hash_files(select_bluray_files(mountpoint))
