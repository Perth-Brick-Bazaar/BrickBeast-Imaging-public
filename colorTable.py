# ------------------------------------------------------------
# 🧱 Tool: color_metadata.py
# Purpose: Handles external color metadata for BrickBeast’s diagnostic registry
# Scope: Loads, updates, and saves color metadata linked by color_id
# Features:
#   - Loads metadata from JSON file
#   - Updates metadata entries by color_id
#   - Retrieves metadata for diagnostic use
#   - Saves updated metadata to disk
# Created by: Craig Wilson / Copilot
# Last Updated: 2025-09-04
# ------------------------------------------------------------
import json
import os

def load_color_table(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_color_metadata(filepath, color_table):
    with open(filepath, "w") as f:
        json.dump(color_table, f, indent=2)

def update_color_metadata(color_table, color_id, metadata):
    entry = color_table.setdefault(str(color_id), {})
    entry.update(metadata)
    return entry

def get_color_metadata(color_table, color_id):
    return color_table.get(str(color_id), {})
