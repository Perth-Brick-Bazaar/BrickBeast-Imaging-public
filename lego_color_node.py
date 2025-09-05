class LegoColorNode:
    def __init__(self, name, number_id, hsv_anchor):
        self.name = name
        self.number_id = number_id
        self.hsv_anchor = hsv_anchor
        self.samples = []
        self.area_size = 1.0
        self.confidence = None

    def add_sample(self, hsv_sample):
        self.samples.append(hsv_sample)
        # Do NOT update anchor automatically!
        self._update_area_and_confidence(hsv_sample)

    def recalibrate_anchor(self, new_hsv_anchor):
        self.hsv_anchor = new_hsv_anchor
        # Optionally recalculate area/confidence for all samples

    # ... rest as before ...