# ------------------------------------------------------------
# 🧱 Tool: arraynodelogic.py
# Purpose: Defines node-level behavior for BrickBeast's perceptual color grid
# Scope: Manages pole zones, sample ingestion, neighbor assignment, and grid metadata
# Features:
#   - Flags perceptual pole zones with locked centroids
#   - Ingests samples with exposure-aware logic
#   - Assigns neighbor relationships across HSV space
#   - Logs near-pole hits for diagnostic review
# Created by: Craig Wilson / Copilot
# Last Updated: 2025-09-04
# ------------------------------------------------------------

import json

# ----------------------------
# Pole Zone Setup
# ----------------------------

def set_pole_zone(grid, h, s, v):
    grid[(h, s, v)] = {
        "color_id": None,
        "sample_density": 0,
        "pole_locked": True,
        "neighbors": [],
        "samples": [],
        "near_pole_hits": []
    }


# ----------------------------
# Neighbor Assignment
# ----------------------------

def assign_neighbors(grid, h, s, v, neighbor_ids):
    node = grid.setdefault((h, s, v), {
        "color_id": None,
        "sample_density": 0,
        "pole_locked": False,
        "neighbors": [],
        "samples": [],
        "near_pole_hits": []
    })
    node["neighbors"] = neighbor_ids


# ----------------------------
# Sample Ingestion
# ----------------------------

def ingest_sample(sample, grid):
    """
    Ingests a single HSV sample into the reference grid.
    Anchors it, logs drift, and returns diagnostic result.

    Args:
        sample (dict): {"h": int, "s": int, "v": int, "source": str}
        grid (dict): Reference grid keyed by (h, s, v)

    Returns:
        dict: {
            "color_id": int,
            "confidence": float,
            "drift": [int, int, int]
        }
    """
    h, s, v = sample["h"], sample["s"], sample["v"]
    source = sample.get("source", "unknown")

    # Step 1: Find closest anchor
    best_match = None
    min_drift = float("inf")

    for key, node in grid.items():
        anchor_h, anchor_s, anchor_v = node["anchor"]
        drift = [h - anchor_h, s - anchor_s, v - anchor_v]
        magnitude = sum(abs(d) for d in drift)

        if magnitude < min_drift:
            min_drift = magnitude
            best_match = {
                "color_id": node["color_id"],
                "drift": drift,
                "confidence": max(0, 1 - magnitude / 765)  # Normalize over max drift
            }

    # Step 2: Log sample to node (optional)
    if best_match:
        grid_key = (h, s, v)
        node = grid.get(grid_key)
        if node:
            node.setdefault("samples", []).append(sample)

    return best_match or {
        "color_id": None,
        "confidence": 0.0,
        "drift": [0, 0, 0]
    }
