from inspect import getmembers, isclass, isabstract

import coffees
from dregs_container import DregsContainer
from water_supply import WaterSupply


class CoffeeMachine(object):
    coffee_programs = {}  # TODO: add typing - key: str, val: class

    def __init__(self, water_supply):
        self.water_supply = water_supply()
        self.dregs = DregsContainer()
        self.is_ready()  # TODO: check if machine is ready
        self._load_coffee_programs()

    def _load_coffee_programs(self):
        classes = getmembers(coffees,
                             lambda c: isclass(c) and not isabstract(c))
        for name, klass in classes:
            if isclass(klass) and issubclass(klass, coffees.AbcCoffee):
                self.coffee_programs.update({name: klass})

    def is_ready(self):
        # TODO: check grains
        return all(
            (isinstance(self.water_supply, WaterSupply),
             isinstance(self.dregs, DregsContainer),)
        )
