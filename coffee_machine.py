from inspect import getmembers, isclass, isabstract

import coffees
from dregs_container import DregsContainer
from water_supply import WaterSupply


class CoffeeGrinder(object):
    def __init__(self, capacity, level):
        self.capacity = capacity
        self._level = level

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, amount):
        self._level = amount

    def refill(self, amount):
        self._level += amount

    def grind(self, amount):
        self._level -= amount
        return amount


class CoffeeMachine(object):
    coffee_programs = {}  # TODO: add typing - key: str, val: class

    def __init__(self, water_supply):
        self.water_supply = water_supply()
        self.dregs = DregsContainer(500)  # TODO: get from settings
        self.grinder = CoffeeGrinder(1000, 1000)  # TODO: get from settings
        self.is_ready()
        self._load_coffee_programs()

    def _load_coffee_programs(self):
        classes = getmembers(coffees,
                             lambda c: isclass(c) and not isabstract(c))
        for name, klass in classes:
            if isclass(klass) and issubclass(klass, coffees.AbcCoffee):
                self.coffee_programs.update({name: klass})

    def is_ready(self):
        return all(
            (isinstance(self.grinder, CoffeeGrinder),
             isinstance(self.water_supply, WaterSupply),
             isinstance(self.dregs, DregsContainer))
        )
