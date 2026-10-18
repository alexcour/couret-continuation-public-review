"""COD-H-01 permission-first file admission. This code never decodes image pixels.

Records supplied by a researcher are *assertions*, not authorization evidence.
No output from this module can certify access rights, spectral quality, or K1.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import os
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

SCHEMA = "codh01-msi-intake-v1"
DOI = "10.5525/gla.researchdata.1865"
UNKNOWN = "non fourni"
ROLES = {"raw_band", "dark_frame", "flat_frame", "processed_reference", "control"}
SCOPES = {"inspect", "process", "derive", "crop", "share_scientific", "publish"}
STATES = {"pending", "granted", "denied", "expired"}
REVIEW_STATES = {"pending", "documented"}
HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")


class ManifestError(ValueError):
    """Invalid or untrusted manifest structure, not missing provider metadata."""


def _required(d: dict, keys: tuple[str, ...], where: str):
    if not isinstance(d, dict):
        raise ManifestError(f"{where} must be a JSON object")
    missing = [key for key in keys if key not in d]
    if missing:
        raise ManifestError(f"{where} missing keys: {', '.join(missing)}")


def _unknown(x: Any) -> bool:
    return x is None or x == "" or x == UNKNOWN


def _relative_path(text: str) -> PurePosixPath:
    if not isinstance(text, str) or "\\" in text or "\x00" in text or ":" in text:
        raise ManifestError("unsafe/invalid POSIX relative path")
    # Reject absolute paths, dot segments, empty parts and simple traversal.
    if not text or text.startswith("/") or any(part in ("", ".", "..") for part in text.split("/")):
        raise ManifestError("unsafe relative path")
    p = PurePosixPath(text)
    if p.is_absolute():
        raise ManifestError("absolute paths are forbidden")
    return p


def parse_manifest(data: dict) -> dict:
    _required(data, ("schema", "dataset", "authorization", "assets"), "root")
    if data["schema"] != SCHEMA:
        raise ManifestError("unknown manifest schema")
    ds = data["dataset"]
    _required(ds, ("doi", "requested_folio", "requested_surface", "supplier_crosswalk"), "dataset")
    if ds["doi"] != DOI:
        raise ManifestError("dataset DOI must be the restricted MSI collection, not TEI 2105")
    if ds["requested_folio"] != "86v" or ds["requested_surface"] != "Coislin 202, 11rT":
        raise ManifestError("unexpected requested folio/surface; investigate rather than auto-mapping")
    if ds["supplier_crosswalk"] not in ("pending", "documented"):
        raise ManifestError("supplier_crosswalk must be pending or documented")
    au = data["authorization"]
    _required(au, ("status", "grantor", "evidence_reference", "allowed_operations",
                   "rights_review", "crosswalk_review"), "authorization")
    if au["status"] not in STATES:
        raise ManifestError("unrecognized authorization state")
    if not isinstance(au["allowed_operations"], list) or len(set(map(str, au["allowed_operations"]))) != len(au["allowed_operations"]):
        raise ManifestError("authorization.allowed_operations must be a unique list")
    if not all(isinstance(x, str) and x in SCOPES for x in au["allowed_operations"]):
        raise ManifestError("unknown permission scopes")
    for name in ("rights_review", "crosswalk_review"):
        r = au[name]
        _required(r, ("status", "reviewer", "record_reference"), "authorization."+name)
        if r["status"] not in REVIEW_STATES:
            raise ManifestError(f"invalid {name} status")
    if not isinstance(data["assets"], list) or len(data["assets"]) > 500:
        raise ManifestError("assets must be a bounded list")
    paths, ids = set(), set()
    for i, asset in enumerate(data["assets"]):
        where = f"assets[{i}]"
        _required(asset, ("supplier_file_id", "relative_path", "role", "folio", "surface",
                          "band_id", "wavelength_nm", "width", "height", "bit_depth",
                          "orientation", "mirror", "capture_date", "flat_frame_id",
                          "dark_frame_id", "supplier_sha256", "supplier_bytes",
                          "license", "credit"), where)
        aid = asset["supplier_file_id"]
        if _unknown(aid) or not isinstance(aid, str) or aid in ids:
            raise ManifestError(f"{where}: missing/duplicate supplier ID")
        ids.add(aid)
        path = str(_relative_path(asset["relative_path"]))
        if path in paths:
            raise ManifestError("duplicate asset paths")
        paths.add(path)
        if asset["role"] not in ROLES:
            raise ManifestError("unrecognized file role")
        if (asset["folio"], asset["surface"]) not in (
                ("86v", "Coislin 202, 11rT"),
                ("87r", "Coislin 202, 11r"),
                (UNKNOWN, UNKNOWN)):
            raise ManifestError("unexpected folio/surface pair; request supplier crosswalk")
        size = asset["supplier_bytes"]
        if size != UNKNOWN and (type(size) is not int or size <= 0):
            raise ManifestError("supplier_bytes must be positive integer or 'non fourni'")
        h = asset["supplier_sha256"]
        if h != UNKNOWN and (not isinstance(h, str) or not HEX64.fullmatch(h)):
            raise ManifestError("supplier_sha256 must be lowercase/uppercase hex SHA256 or 'non fourni'")
        for key in ("width", "height", "bit_depth"):
            value = asset[key]
            if value != UNKNOWN and (type(value) is not int or value <= 0):
                raise ManifestError(f"{key} must be positive integer or 'non fourni'")
        w = asset["wavelength_nm"]
        if w != UNKNOWN and (isinstance(w, bool) or not isinstance(w, (int, float)) or not 100 <= w <= 3000):
            raise ManifestError("wavelength_nm must be plausible numeric or 'non fourni'")
        if asset["mirror"] not in (UNKNOWN, "yes", "no"):
            raise ManifestError("mirror must be yes/no/non fourni")
    return data


def _review_documented(review: dict) -> bool:
    return (review["status"] == "documented" and not _unknown(review["reviewer"])
            and not _unknown(review["record_reference"]))


def evaluate(data: dict) -> dict:
    """Metadata-only: returns blockers without reading any image or checking license authenticity."""
    m = parse_manifest(data)
    blockers: list[str] = []
    warnings: list[str] = []
    ds, au, assets = m["dataset"], m["authorization"], m["assets"]
    if au["status"] != "granted":
        blockers.append("ACCESS: grant absent/denied/expired; receipt is not permission")
    if _unknown(au["grantor"]) or _unknown(au["evidence_reference"]):
        blockers.append("ACCESS: named grantor and private evidence reference missing")
    if "inspect" not in au["allowed_operations"]:
        blockers.append("ACCESS: no explicit permission even to inspect local restricted files")
    if not _review_documented(au["rights_review"]):
        blockers.append("ACCESS: recorded human review of rights and scope missing")
    if not _review_documented(au["crosswalk_review"]) or ds["supplier_crosswalk"] != "documented":
        blockers.append("MAPPING: 86v / Coislin 202 11rT supplier crosswalk is unverified")
    if not assets:
        blockers.append("FILES: no supplier asset inventory received")
    for i, asset in enumerate(assets):
        src = f"assets[{i}]({asset['supplier_file_id']})"
        # License and attribution are access-related; never read bytes without them.
        for key in ("folio", "surface", "credit", "license"):
            if _unknown(asset[key]):
                blockers.append(f"RIGHTS/MAPPING: {src} missing {key}")
        for key in ("supplier_bytes", "supplier_sha256"):
            if _unknown(asset[key]):
                warnings.append(f"REFERENCE: {src} missing supplier {key}; receipt can be hashed locally but not vendor-verified")
        for key in ("capture_date", "orientation", "mirror"):
            if _unknown(asset[key]):
                warnings.append(f"METADATA: {src} missing {key}; image analysis prohibited")
        if asset["role"] == "raw_band":
            for key in ("band_id", "width", "height", "bit_depth"):
                if _unknown(asset[key]):
                    warnings.append(f"METADATA: {src} missing {key}; image analysis prohibited")
            if _unknown(asset["wavelength_nm"]):
                warnings.append(f"SPECTRAL: {src} wavelength not supplied; no spectral inference")
            if _unknown(asset["dark_frame_id"]) or _unknown(asset["flat_frame_id"]):
                warnings.append(f"CALIBRATION: {src} dark/flat references absent; no radiometric claims")
    # Even with documented assertions, automated code does not validate grant signatures.
    status = "HOLD" if blockers else "MANUAL_EVIDENCE_REVIEW_REQUIRED"
    return {"schema": SCHEMA, "gate": status, "blockers": blockers, "warnings": warnings,
            "asset_count": len(assets), "can_read_local_files": not blockers,
            "authorization_authenticity_machine_verified": False,
            "real_msi_processed": False, "k1_reconstruction": "NONE",
            "policy": "Human must independently inspect original written grant, local identity and scope. Never share raw pixels automatically."}


def _safe_file(root: Path, relative: str) -> Path:
    base = root.resolve(strict=True)
    if not base.is_dir():
        raise ValueError("source root is not a directory")
    p = base.joinpath(*_relative_path(relative).parts)
    # Path.is_symlink() catches the final link. Parents are checked via resolve.
    if p.is_symlink() or not p.resolve(strict=True).is_relative_to(base) or not p.is_file():
        raise ValueError("invalid or escaping file; symlinks forbidden")
    for parent in p.parents:
        if parent == base:
            break
        if parent.is_symlink():
            raise ValueError("symlink component forbidden")
    return p


def _hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def verify_local(data: dict, root: Path) -> dict:
    """Read only for authorized *locally staged* files; never uploads or decodes.

    IMPORTANT: this verifies self-attested grant metadata, not its authenticity.
    A human must first confirm the source's grant and scope independently.
    """
    status = evaluate(data)
    if status["gate"] != "MANUAL_EVIDENCE_REVIEW_REQUIRED":
        raise PermissionError("Fail closed: access/mapping/metadata intake gate is blocked; no file bytes opened")
    results = []
    for entry in data["assets"]:
        path = _safe_file(root, entry["relative_path"])
        # Hash first, even if no supplier checksum was issued. This is a new,
        # private *receipt* fingerprint, NOT proof of remote integrity.
        current_bytes = path.stat().st_size
        observed_hash = _hash(path)
        expected_bytes, expected_hash = entry["supplier_bytes"], entry["supplier_sha256"]
        size_matches = None if expected_bytes == UNKNOWN else current_bytes == expected_bytes
        sha_matches = None if expected_hash == UNKNOWN else observed_hash.lower() == expected_hash.lower()
        result_state = ("FAIL" if (size_matches is False or sha_matches is False)
                        else "UNVERIFIED_REFERENCE" if (size_matches is None or sha_matches is None)
                        else "PASS")
        results.append({"supplier_file_id": entry["supplier_file_id"],
                        "observed_bytes": current_bytes, "observed_sha256": observed_hash,
                        "size_matches_supplier": size_matches,
                        "sha256_matches_supplier": sha_matches, "integrity_status": result_state})
    status["local_integrity"] = results
    if any(x['integrity_status'] == 'FAIL' for x in results):
        status["gate"] = "HOLD_INTEGRITY"
    elif any(x['integrity_status'] == 'UNVERIFIED_REFERENCE' for x in results):
        status["gate"] = "HOLD_REFERENCE_UNAVAILABLE"
    else:
        status["gate"] = "HUMAN_REVIEW_REQUIRED"
    status["can_read_local_files"] = False  # This is NOT a processing authorization.
    status["file_hashes_recomputed"] = True
    return status



def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=('evaluate', 'verify-local'))
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--source-root', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args(argv)
    try:
        if args.command == 'verify-local' and args.output is None:
            raise ManifestError('--output must point to a private receipt report')
        data = json.loads(args.manifest.read_text(encoding='utf-8'))
        if args.command == 'verify-local':
            if args.source_root is None:
                raise ManifestError('--source-root required for verify-local')
            report = verify_local(data, args.source_root)
        else:
            report = evaluate(data)
    except (ManifestError, PermissionError, OSError, ValueError, TypeError, KeyError) as e:
        # Keep output free from restricted local paths/content.
        report = {"schema": SCHEMA, "gate": "HOLD_ERROR", "error_type": type(e).__name__,
                  "message": str(e).splitlines()[0], "real_msi_processed": False,
                  "k1_reconstruction": "NONE"}
    encoded = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.output:
        if args.output.exists():
            raise FileExistsError('cannot overwrite existing evidence report')
        # Exclusive creation and strict permissions, even with a permissive umask.
        fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            out.write(encoded)
    else:
        print(encoded, end='')
    return 0 if report['gate'] in ('MANUAL_EVIDENCE_REVIEW_REQUIRED', 'HUMAN_REVIEW_REQUIRED') else 2


if __name__ == '__main__':
    raise SystemExit(main())