## Anchor Update Policy

- **Color anchors** (the reference center for each LEGO color) are only updated by programmer review or periodic calibration against released LEGO parts.
- **Samples** are recorded for each color node and used to analyze drift or device/environment variation.
- **Compensation logic** maintains robust colorID output for store integration, regardless of sample drift.

### Calibration Workflow

1. Review sample drift for each color node periodically (via code or manual inspection).
2. Update anchor location only when necessary to maintain real-world color associations.
3. Log changes for traceability and future refinements.