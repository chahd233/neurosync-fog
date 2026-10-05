# PROTOTYPE thresholds - NOT clinically validated
FI_NORMAL = 1.0      # below this = normal walking
FI_FREEZE = 2.0      # at/above this = possible freeze
FI_RELEASE = 1.2     # cue stays on until FI drops below this
CONSECUTIVE = 2      # windows needed to trigger

class FOGDetector:
    def __init__(self):
        self.count = 0
        self.cue = False

    def update(self, fi):
        """Feed one FI value. Returns (state, cue_active)."""
        if not self.cue:
            self.count = self.count + 1 if fi >= FI_FREEZE else 0
            if self.count >= CONSECUTIVE:
                self.cue = True
        elif fi < FI_RELEASE:
            self.cue, self.count = False, 0

        if self.cue:
            state = "FOG_DETECTED"
        elif fi >= FI_FREEZE:
            state = "PRE_FREEZE"
        elif fi < FI_NORMAL:
            state = "NORMAL"
        else:
            state = "UNCERTAIN"
        return state, self.cue
