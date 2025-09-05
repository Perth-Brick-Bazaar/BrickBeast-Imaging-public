# ------------------------------------------------------------
# 🧱 Tool: load_area_array.py
# Purpose: Ingests samples into BrickBeast’s perceptual grid and logs drift metrics
# Scope: Anchors grid nodes, tracks HSV drift, and computes confidence scores
# Features:
#   - Anchors grid zones on first sample hit
#   - Logs HSV drift relative to anchor
#   - Updates sample density and node history
#   - Computes confidence score based on drift magnitude
# Created by: Craig Wilson / Copilot
# Last Updated: 2025-09-04
# ------------------------------------------------------------

def load_area_array(samples, grid, drift_threshold=(10, 10, 10)):
    results = []

    for sample in samples:
        h, s, v = sample["h"], sample["s"], sample["v"]
        node = grid.setdefault((h, s, v), {
            "color_id": None,
            "sample_density": 0,
            "pole_locked": False,
            "samples": [],
            "anchor": None,
            "drift": []
        })

        # Anchor if needed
        if node["anchor"] is None:
            node["anchor"] = sample

        # Log drift
        anchor = node["anchor"]
        drift = {
            "dh": abs(sample["h"] - anchor["h"]),
            "ds": abs(sample["s"] - anchor["s"]),
            "dv": abs(sample["v"] - anchor["v"])
        }
        node["drift"].append(drift)

        # Update density and samples
        node["sample_density"] += 1
        node["samples"].append(sample)

        # Confidence scoring
        total_drift = drift["dh"] + drift["ds"] + drift["dv"]
        confidence = max(0, 255 - total_drift) / 255

        results.append({
            "center": (h, s, v),
            "color_id": node["color_id"],
            "confidence": round(confidence, 3),
            "drift": drift
        })

    return results
