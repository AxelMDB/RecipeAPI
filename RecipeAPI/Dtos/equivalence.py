class EquivalenceDto(object):
    def __init__(self, unit_1: str = "", unit_2: str = "", multiplier: float = 1.0):
        self.unit_1 = unit_1
        self.unit_2 = unit_2
        self.multiplier = multiplier