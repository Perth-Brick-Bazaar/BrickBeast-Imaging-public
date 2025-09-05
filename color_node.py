# 🧱 BrickBeast ColorNode — Unified Color Node Class
#
# Purpose:
#   Stores and manages perceptual color anchors (HSV/RGB), sample ingestion, drift logic, confidence scoring,
#   and metadata for BrickBeast color registry and matching.
#
# Scope:
#   - Stores color anchors and drift center
#   - Ingests samples, updates drift and confidence
#   - Supports tolerance checks and drift locking
#   - Links metadata for diagnostics
#
# Linked Files:
#   - Imports: colorreferance.py (legacy logic), colorTable.py (metadata), reference_loader.py (data loader),
#              arraynodelogic.py (node manager), utils.py (color conversion)
#   - Reads: bricklink_colours.json, ColorReference.json (reference data sources)
#   - Writes: Sample logs, drift records, output images (filenames may vary with part/timestamp)
#   - Note: Output filenames may vary; update consumers if naming logic changes.
#
# Output:
#   - Color ID and confidence for matched color node
#   - Drift center and sample history (for diagnostics)
#
# Notes:
#   - No weighing by color amount; matching is by confidence.
#   - Consensus color ID is reached after multiple images.
#   - Masking logic is handled in a separate module.
#
# Author: Craig Wilson / Copilot
# Last Updated: 2025-09-05

import numpy as np

class ColorNode:
    def __init__(self, color_id, name, rgb_anchor, hsv_anchor, type_, tolerance, max_drift, metadata=None):
        self.color_id = color_id
        self.name = name
        self.rgb_anchor = np.array(rgb_anchor, dtype=float)
        self.hsv_anchor = np.array(hsv_anchor, dtype=float)
        self.type = type_
        self.tolerance = tolerance  # dict: {"hue": int, "sat": int, "val": int}
        self.max_drift = max_drift
        self.samples = []
        self.drift_center = self.hsv_anchor.copy()
        self.drift_locked = False
        self.confidence_avg = 1.0
        self.last_drift_vector = np.zeros(3)
        self.metadata = metadata or {}

    def add_sample(self, hsv_sample):
        self.samples.append(hsv_sample)
        if not self.drift_locked and self.is_within_tolerance(hsv_sample):
            self.apply_drift(hsv_sample)
        self.update_confidence()

    def is_within_tolerance(self, sample_hsv):
        sample = np.array(sample_hsv, dtype=float)
        return all(
            abs(sample[i] - self.drift_center[i]) <= self.tolerance[key]
            for i, key in enumerate(["hue", "sat", "val"])
        )

    def apply_drift(self, sample_hsv, dampener=0.2):
        sample = np.array(sample_hsv, dtype=float)
        offset = (sample - self.drift_center) * dampener
        self.drift_center += offset
        self.last_drift_vector = offset

    def update_confidence(self):
        if not self.samples:
            self.confidence_avg = None
            return
        avg_dist = np.mean([np.linalg.norm(np.array(s) - self.drift_center) for s in self.samples])
        self.confidence_avg = 1 / (1 + avg_dist)  # Example scaling

    def to_dict(self):
        return {
            "color_id": self.color_id,
            "name": self.name,
            "rgb_anchor": self.rgb_anchor.tolist(),
            "hsv_anchor": self.hsv_anchor.tolist(),
            "drift_center": self.drift_center.tolist(),
            "type": self.type,
            "tolerance": self.tolerance,
            "max_drift": self.max_drift,
            "samples": self.samples,
            "confidence_avg": self.confidence_avg,
            "last_drift_vector": self.last_drift_vector.tolist(),
            "drift_locked": self.drift_locked,
            "metadata": self.metadata
        }