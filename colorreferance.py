# ------------------------------------------------------------
# 🧱 Tool: colorreferance.py
# Purpose: Manages BrickBeast’s color registry and reference logic for perceptual drift
# Scope: Defines ColorReference objects, calibrates drift centers, and saves registry state
# Features:
#   - Loads color data from ColorReference.json
#   - Applies dampened drift logic across registry entries
#   - Validates sample tolerance and drift eligibility
#   - Saves calibrated registry and timestamped backup
# Created by: Craig Wilson / Copilot
# Last Updated: 2025-09-04
# ------------------------------------------------------------

import json
import os
from datetime import datetime
import numpy as np

class ColorReference:
    def __init__(self, data):
        self.color_id = data["color_id"]
        self.name = data["color_name"]

        self.reset_center = np.array(data["reset_center"], dtype=float)
        self.anchor_center = np.array(data["anchor_center"], dtype=float)
        self.drift_center = np.array(data["drift_center"], dtype=float)

        self.max_drift = data.get("max_drift", 5.0)
        self.tolerance = data["tolerance"]

        self.edge_ratio = data.get("edge_ratio", 0.0)
        self.confidence_avg = data.get("confidence_avg", 1.0)
        self.last_drift_vector = np.array(data.get("last_drift_vector", [0, 0, 0]), dtype=float)
        self.drift_locked = data.get("drift_locked", False)

    def to_dict(self):
        return {
            "color_id": self.color_id,
            "color_name": self.name,
            "reset_center": self.reset_center.tolist(),
            "anchor_center": self.anchor_center.tolist(),
            "drift_center": self.drift_center.tolist(),
            "max_drift": self.max_drift,
            "tolerance": self.tolerance,
            "edge_ratio": self.edge_ratio,
            "confidence_avg": self.confidence_avg,
            "last_drift_vector": self.last_drift_vector.tolist(),
            "drift_locked": self.drift_locked
        }

    def is_within_tolerance(self, sample_hsv):
        sample = np.array(sample_hsv, dtype=float)
        return all(
            abs(sample[i] - self.drift_center[i]) <= self.tolerance[key]
            for i, key in enumerate(["hue", "sat", "val"])
        )

    def drift_magnitude(self):
        return np.linalg.norm(self.drift_center - self.anchor_center)

    def can_drift(self, sample_hsv, registry):
        if self.drift_locked:
            return False
        sample = np.array(sample_hsv, dtype=float)
        proposed = self.drift_center + (sample - self.drift_center) / 20
        for other in registry.values():
            if other.color_id == self.color_id:
                continue
            dist = np.linalg.norm(proposed - other.drift_center)
            if dist < self.max_drift + other.max_drift:
                return False
        return np.linalg.norm(proposed - self.anchor_center) <= self.max_drift

    def apply_drift(self, sample_hsv, dampener=0.2):
        sample = np.array(sample_hsv, dtype=float)
        offset = (sample - self.drift_center) * dampener
        self.drift_center += offset
        self.last_drift_vector = offset


class ColorRegistry:
    def __init__(self, path="ColorReference.json"):
        self.path = path
        self.registry = {}
        self.load_and_calibrate()

    def load_and_calibrate(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Reference file not found: {self.path}")

        with open(self.path, 'r') as f:
            raw_data = json.load(f)

        for entry in raw_data:
            ref = ColorReference(entry)
            self.registry[ref.color_id] = ref

        self.calibrate()

    def dampened_drift_vector(self, ref, dampener=0.2):
        target = ref.drift_center
        vectors = []

        for other in self.registry.values():
            if other.color_id == ref.color_id:
                continue

            neighbor = other.drift_center
            vector = target - neighbor
            distance = np.linalg.norm(vector)

            if distance < ref.max_drift + other.max_drift:
                unit_vector = vector / distance
                safe_distance = distance - other.max_drift
                damped_vector = unit_vector * safe_distance * dampener
                vectors.append(damped_vector)

        if vectors:
            return np.mean(vectors, axis=0)
        return np.array([0.0, 0.0, 0.0])

    def calibrate(self, threshold=0.01, max_passes=10, dampener=0.2):
        for _ in range(max_passes):
            changes = 0
            for ref in self.registry.values():
                vector = self.dampened_drift_vector(ref, dampener)
                projected = ref.drift_center + vector
                if np.linalg.norm(projected - ref.drift_center) > threshold:
                    ref.drift_center = projected
                    ref.last_drift_vector = vector
                    changes += 1
            if changes == 0:
                break

    def save(self):
        with open(self.path, 'w') as f:
            json.dump([ref.to_dict() for ref in self.registry.values()], f, indent=2)

        date_stamp = datetime.now().strftime("%Y-%m-%d")
        backup_path = f"ColorReference_backup_{date_stamp}.json"
        with open(backup_path, 'w') as f:
            json.dump([ref.to_dict() for ref in self.registry.values()], f, indent=2)
