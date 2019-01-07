from coffee_machine.config import get_config


class Ingredient(object):
    # TODO: make __dict__ variables immutable
    pass


class Coffee(Ingredient):
    _config = get_config()['espresso_unit']

    def __init__(self, units, additional_water=0):
        self._units = units
        self.grains_amount = None
        self.water_amount = None
        self.additional_water = additional_water
        self.set_amounts()

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value
        self.set_amounts()

    def set_amounts(self):
        self.grains_amount = self._config['coffee_grams'] * self.units
        water_proportion = self.grains_amount / self._config['ratio_coffee2water']
        self.water_amount = water_proportion + self.additional_water


class Milk(Ingredient):
    def __init__(self, amount):
        self.amount = amount
