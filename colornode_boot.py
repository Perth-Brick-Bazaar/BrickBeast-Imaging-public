# ------------------------------------------------------------
# 🧱 Tool: bcolornode_boot.py
# Purpose: Boots BrickBeast’s perceptual grid with pole zones and neighbor logic
# Scope: Initializes grid structure, flags pole zones, and assigns sample neighbors
# Features:
#   - Calls initialize_reference_grid() from arraynodelogic
#   - Flags black and white pole zones with locked centroids
#   - Assigns example neighbor relationships for diagnostic linkage
#   - Prints boot confirmation and returns grid object
# Created by: Craig Wilson / Copilot
# Last Updated: 2025-09-04
# ------------------------------------------------------------

import arraynodelogic as gridlogic 
import json

def boot_brickbeast():
    # Initialize grid
    grid = gridlogic.initialize_reference_grid()

    # Define pole zones
    gridlogic.set_pole_zone(grid, 0, 0, 0)         # Black
    gridlogic.set_pole_zone(grid, 255, 255, 255)   # White

    # Assign neighbors (example only)
    gridlogic.assign_neighbors(grid, 160, 160, 160, [85, 9, 88, 2])

    print("BrickBeast booted with stable grid.")
    return grid

if __name__ == "__main__":
    grid = boot_brickbeast()
