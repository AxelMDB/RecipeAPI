from .unit import UnitDto


class IngredientDto(object):
    """description of class"""
    def __init__(self, name: str = "", main_unit: UnitDto = UnitDto()):
        self.name = name
        sef.main_unit = main_unit
