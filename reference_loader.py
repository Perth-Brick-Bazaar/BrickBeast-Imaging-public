# ------------------------------------------------------------
# 🧱 Tool: reference_loader.py
# Purpose: Initializes BrickBeast’s perceptual grid using BrickLink color anchors
# Scope: Loads color data, builds grid nodes, and saves reference metadata
# Features:
#   - Loads BrickLink color data from JSON
#   - Builds anchored grid nodes with pole locking
#   - Saves grid to bricklink_reference_grid.json
#   - Saves metadata to bricklink_metadata.json
# Created by: Craig Wilson / Copilot
# Last Updated: 2025-09-04
# ------------------------------------------------------------
import json

def initialize_reference_grid(colour_json_path, output_grid_path, output_metadata_path):
    with open(colour_json_path, "r") as f:
        colour_data = json.load(f)

    grid = {}
    metadata = {}

    for cid_str, entry in colour_data.items():
        cid = int(cid_str)
        h, s, v = entry["hsv"]

        # Build grid node
        grid[(h, s, v)] = {
            "color_id": cid,
            "sample_density": 0,
            "pole_locked": True,
            "samples": [],
            "anchor": {
                "h": h,
                "s": s,
                "v": v
            },
            "drift": []
        }

        # Build metadata entry
        metadata.setdefault(str(cid), {})["BrickLink"] = {
            "name": entry["colourName"],
            "hex": entry["hex"],
            "type": entry["type"],
            "rgb": entry["rgb"],
            "hsv": entry["hsv"]
        }

    # Save grid with stringified keys
    serializable_grid = {
        f"{h},{s},{v}": data for (h, s, v), data in grid.items()
    }
    with open(output_grid_path, "w") as f:
        json.dump(serializable_grid, f, indent=2)

    # Save metadata
    with open(output_metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return grid, metadata

def load_bricklink_colours(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def build_reference_grid(colour_data):
    grid = {}
    for cid_str, entry in colour_data.items():
        cid = int(cid_str)
        h, s, v = entry["hsv"]
        grid[(h, s, v)] = {
            "color_id": cid,
            "sample_density": 0,
            "pole_locked": True,
            "samples": [],
            "anchor": {
                "h": h,
                "s": s,
                "v": v,
                "source": "BrickLink",
                "name": entry["colourName"],
                "hex": entry["hex"],
                "type": entry["type"]
            },
            "drift": []
        }
    return grid

def save_reference_grid(filepath, grid):
    # Convert tuple keys to string for JSON compatibility
    serializable_grid = {
        f"{h},{s},{v}": data for (h, s, v), data in grid.items()
    }
    with open(filepath, "w") as f:
        json.dump(serializable_grid, f, indent=2)
