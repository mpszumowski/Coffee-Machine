from config import get_config


class Ingredient(object):
    # TODO: make __dict__ variables immutable
    pass


class Coffee(Ingredient):
    _config = get_config()['espresso_unit']

    def __init__(self, coffee_units, additional_water=0):
        self.coffee = self._config['coffee_grams'] * coffee_units
        water = self.coffee / self._config['ratio_coffee2water']
        self.water = water + additional_water


class Milk(Ingredient):
    def __init__(self, amount):
        self.amount = amount
