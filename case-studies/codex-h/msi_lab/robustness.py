"""COD-H-01 adversarial MSI laboratory. Synthetic pixels only, no glyph recognition.

No public manuscript file is loaded. This module deliberately demonstrates that
multiband corroboration, calibrated brightness and PCA stability are not a
sufficient test for an ancient character or an ink attribution.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from scipy import ndimage

SIZE = 96
ROI = (slice(37, 58), slice(27, 33))
BLANK = (slice(65, 86), slice(64, 70))
SCENARIOS = ("signal", "blank", "shared_stain", "correlated_stripe", "illumination")


def fixtures(scenario: str, seed: int = 20261018) -> tuple[np.ndarray, dict]:
    """Return an *invented*, uncalibrated four-band intensity cube and truth label."""
    if scenario not in SCENARIOS:
        raise ValueError("unsupported synthetic scenario")
    rng = np.random.default_rng(seed)
    yy, xx = np.indices((SIZE, SIZE))
    background = 0.55 + 0.01 * np.sin(xx / 18) + 0.008 * np.cos(yy / 16)
    ink = np.zeros((SIZE, SIZE))
    ink[37:58, 27:33] = 1
    ink[54:58, 27:48] = 1
    stain = np.exp(-0.5 * (((xx - 30) / 10) ** 2 + ((yy - 46) / 16) ** 2))
    stripe = np.zeros((SIZE, SIZE))
    stripe[:, 27:33] = 1  # line-scan/camera stripe, not writing
    shadow = np.exp(-0.5 * (((xx - 29) / 12) ** 2 + ((yy - 48) / 19) ** 2))
    coherent = ndimage.gaussian_filter(rng.normal(size=(SIZE, SIZE)), 1.8)
    coherent /= max(coherent.std(), 1e-10)
    bands = []
    for i in range(4):
        a = background.copy()
        if scenario == "signal":
            a -= (0.12 + 0.012 * i) * ink
        elif scenario == "shared_stain":
            a -= (0.19 + 0.003 * i) * stain
        elif scenario == "correlated_stripe":
            a -= (0.13 + 0.004 * i) * stripe
        elif scenario == "illumination":
            a -= (0.18 + 0.002 * i) * shadow
        a += 0.009 * coherent  # shared substrate/sensor structure
        a += rng.normal(0, 0.005, (SIZE, SIZE))  # channel-specific noise
        bands.append(a)
    cube = np.stack(bands, axis=-1)
    return cube, {"origin": "SYNTHETIC_ONLY", "truth": scenario, "seed": seed,
                  "bands": 4, "manuscript_characters_present": False}


def dark_flat_correct(raw: np.ndarray, dark: np.ndarray, flat: np.ndarray,
                      *, saturation: float = 1.0, max_masked: float = 0.01):
    """Fail closed on missing/bad calibration; do not silently clip bad pixels.

    Assumes floating linear digital intensity on [0,1] in THIS synthetic protocol.
    Real MSI requires supplier-specific units and calibration review.
    """
    if any(x is None for x in (raw, dark, flat)):
        raise ValueError("dark and flat frames required")
    raw, dark, flat = (np.asarray(x, dtype=float) for x in (raw, dark, flat))
    if raw.shape != dark.shape or raw.shape != flat.shape or raw.ndim not in (2, 3):
        raise ValueError("calibration shapes must match")
    if not all(np.isfinite(x).all() for x in (raw, dark, flat)):
        raise ValueError("nonfinite calibration values")
    span = flat - dark
    if np.any(span <= 0.03) or not (0 < saturation <= 1):
        raise ValueError("flat-dark span or saturation invalid")
    masked = (raw >= saturation) | (raw < 0)
    fraction = float(np.mean(masked))
    if fraction > max_masked:
        raise ValueError("too many saturated/invalid pixels")
    corrected = (raw - dark) / span
    corrected[masked] = np.nan  # missing signal stays missing
    return corrected, {"masked_fraction": fraction,
                       "flat_dark_span_min": float(span.min()),
                       "photometric_scope": "synthetic_linear_only"}


def contrast_report(cube: np.ndarray, threshold: float = -0.04) -> dict:
    """Known synthetic ROI contrast; NEVER an inference of letters."""
    cube = np.asarray(cube)
    if cube.shape != (SIZE, SIZE, 4) or not np.isfinite(cube).all():
        raise ValueError("synthetic four-band cube required")
    contrasts = (cube[ROI].mean(axis=(0, 1)) - cube[BLANK].mean(axis=(0, 1))).tolist()
    support = int(sum(x < threshold for x in contrasts))
    return {"contrast_by_band": contrasts, "band_support": support,
            "holdout_last_band": contrasts[-1], "threshold": threshold,
            "interpretation": "AMBIGUOUS_ENGINEERING_SIGNAL" if support else "NO_DETECTABLE_FIXTURE_CONTRAST",
            "k1_reading": "NOT_RECONSTRUCTED", "folio": "NOT_APPLICABLE"}


def first_pc_cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Sign-independent cosine of first PC; PCA cannot identify what made a feature."""
    def pc(x):
        if x.ndim != 3 or x.shape[2] != 3 or not np.isfinite(x).all():
            raise ValueError("PCA input must have three finite training bands")
        flat = x.reshape(-1, 3)
        centered = flat - flat.mean(axis=0)
        cov = centered.T @ centered / max(len(centered) - 1, 1)
        eig, vectors = np.linalg.eigh(cov)
        if eig[-1] <= 0 or (eig[-1] - eig[-2]) / eig[-1] < 0.05:
            raise ValueError("leading component ambiguous / degenerate")
        return vectors[:, -1]
    return float(abs(np.dot(pc(a), pc(b))))


def pca_perturbation_report(cube: np.ndarray, *, seed=732, repetitions=32) -> dict:
    """Bootstrap-like synthetic noise/illumination stress, fourth band excluded."""
    if cube.shape != (SIZE, SIZE, 4) or repetitions < 2:
        raise ValueError("four-band cube and >=2 repetitions needed")
    base = cube[:, :, :3]
    rng = np.random.default_rng(seed)
    yy, xx = np.indices((SIZE, SIZE))
    grad = (xx - SIZE / 2) / SIZE
    similarities = []
    for _ in range(repetitions):
        light = 1 + rng.normal(0, 0.02, (1, 1, 3))
        shifted = base * light + grad[:, :, None] * rng.normal(0, 0.01, (1, 1, 3))
        shifted += rng.normal(0, 0.008, shifted.shape)
        similarities.append(first_pc_cosine(base, shifted))
    return {"pc1_abs_cosine_min": min(similarities),
            "pc1_abs_cosine_median": float(np.median(similarities)),
            "perturbation_repetitions": repetitions,
            "pca_fit_channels": [0, 1, 2], "held_out_channel": 3,
            "qualification": "Stability is not evidence of manuscript text"}


def registration_stress(image: np.ndarray, displacement: tuple[float, float],
                        *, max_integer_shift=3, tolerance=0.008) -> dict:
    """Detect fractional displacement that integer-only registration cannot repair.

    Reference is the known synthetic image; no true geometry is inferred.
    """
    ref = np.asarray(image, dtype=float)
    if ref.shape != (SIZE, SIZE):
        raise ValueError("synthetic single band only")
    captured = ndimage.shift(ref, displacement, order=1, mode="nearest")
    mask = np.zeros(ref.shape, bool)
    mask[6:-6, 6:-6] = (abs(ref[6:-6, 6:-6] - np.median(ref)) > 0.025)
    if mask.sum() < 10:
        raise ValueError("insufficient reference texture")
    candidates = []
    for dy in range(-max_integer_shift, max_integer_shift + 1):
        for dx in range(-max_integer_shift, max_integer_shift + 1):
            trial = ndimage.shift(captured, (dy, dx), order=1, mode="nearest")
            rms = float(np.sqrt(np.mean((trial[mask] - ref[mask]) ** 2)))
            candidates.append((rms, dy, dx))
    residual, dy, dx = min(candidates)
    return {"best_integer_correction": [dy, dx], "reference_roi_rmse": residual,
            "tolerance": tolerance, "integer_model_adequate": residual <= tolerance,
            "verification_type": "known_geometry_synthetic_only"}


def synthetic_report(seed=20261018):
    results = {}
    for scenario in SCENARIOS:
        cube, provenance = fixtures(scenario, seed=seed)
        result = contrast_report(cube)
        result["pca_stability"] = pca_perturbation_report(cube)
        result["provenance"] = provenance
        results[scenario] = result
    return {"document": "COD-H-01 G0.12/G0.13", "status": "SYNTHETIC_ONLY",
            "real_MSI_processed": False, "k1_certified": False, "scenarios": results}


if __name__ == "__main__":
    print(json.dumps(synthetic_report(), indent=2, sort_keys=True))
