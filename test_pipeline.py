# ------------------------------------------------------------
# 🧪 Module: test_pipeline.py
# Purpose: Validate intake-to-output flow using one sample source
# Scope: Apply correction (if available), structure sample, anchor, log drift
# Created by: Craig Wilson / Copilot
# Last Updated: 2025-09-04
# ------------------------------------------------------------

from reference_loader import initialize_reference_grid
from colornode_boot import boot_brickbeast
from arraynodelogic import ingest_sample

# Sample input (from one known camera)
raw_sample = {
    "h": 21,
    "s": 79,
    "v": 238,
    "source": "cam_A"
}

# Step 1: Load reference grid
reference_grid = initialize_reference_grid("bricklink_colours.json")

# Step 2: Boot grid (if needed)
boot_brickbeast(reference_grid)

# Step 3: Ingest sample
# If you have multiple ingest_sample variants, use the one that handles single sample intake
result = ingest_sample(raw_sample, reference_grid)

# Step 4: Output diagnostic result
print("Diagnostic Result:")
print(f"  Color ID: {result.get('color_id')}")
print(f"  Confidence: {result.get('confidence')}")
print(f"  Drift: {result.get('drift')}")
