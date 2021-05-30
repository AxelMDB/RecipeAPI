class UnitDto(object):
    """description of class"""
    def __init__(self, unit: str = "", equivalence_units: list = []):
        self.unit = unit
        self.equivalent_ids = equivalence_units
