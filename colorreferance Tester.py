# ------------------------------------------------------------
# 🧱 Tool: drift_red_test.py
# Purpose: Tests drift logic for Red in BrickBeast’s color registry
# Scope: Loads registry, checks drift eligibility, applies update, and saves result
# Features:
#   - Loads ColorRegistry from colorreferance
#   - Targets Red (ID 5) with a direct center match
#   - Applies drift if permitted by registry logic
#   - Saves updated registry state
# Created by: Craig Wilson / Copilot
# Last Updated: 2025-09-04
# ------------------------------------------------------------
from colorreferance import ColorRegistry  # assuming you saved the full scaffold as registry.py

# Load and calibrate
reg = ColorRegistry()

# Sample that lands directly on Red's drift center
sample_hsv = [1.2, 253.5, 127.1]  # matches Red exactly

# Find Red
red = reg.registry[5]

# Apply drift if allowed
if red.can_drift(sample_hsv, reg.registry):
    red.apply_drift(sample_hsv)
    print(f"Red drift updated to: {red.drift_center}")
else:
    print("Drift not allowed for Red")

# Save updated registry
reg.save()
