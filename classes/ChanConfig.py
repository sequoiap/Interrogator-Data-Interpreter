class ChanConfig:

    def __init__(self, channel, dist_comp_enabled, spec_adv_count, threshold, rel_threshold, width_lvl, width, detect_valley):
        self.channel = channel
        self.dist_comp_enabled = dist_comp_enabled
        self.spec_adv_count = spec_adv_count
        self.threshold = threshold
        self.rel_threshold = rel_threshold
        self.width_lvl = width_lvl
        self.width = width
        self.detect_valley = detect_valley
    
    def print(self):
        print("CH " + str(self.channel) + " Configuration:")
        print("\tDistance Compensation Enabled: " + str(self.dist_comp_enabled))
        print("\tSpectral Advantage Count: " + self.spec_adv_count)
        print("\tThreshold: " + self.threshold + " dB")
        print("\tRel. Thresh.: " + self.rel_threshold + " dB")
        print("\tWidth Level: " + self.width_lvl + " dB")
        print("\tWidth: " + self.width + " nm")
        print("\tDetect Valley: " + str(self.detect_valley))
