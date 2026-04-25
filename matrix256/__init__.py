"""matrix256 — reproducible fingerprints for optical discs and filesystem trees.

Each matrix256 algorithm version is a separate submodule:

- ``matrix256.v0`` — structural hash over a fixed list of named metadata files
  (DVD: ``VIDEO_TS.IFO``, ``VTS_NN_0.IFO``; Blu-ray: ``index.bdmv``,
  ``MovieObject.bdmv``, MPLS, CLPI). See ``README.md``.
- ``matrix256.v1`` — filesystem-walk hash over (path, size) records. See
  ``SPEC.md``. Not yet implemented.

Versions produce independent digest spaces; importing code must select a
version explicitly (e.g. ``from matrix256.v0 import select_dvd_files``). The
package itself exposes nothing — there is no implicit "current" version.
"""
