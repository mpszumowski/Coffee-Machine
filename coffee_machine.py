from inspect import getmembers, isclass, isabstract

import coffees
from dregs_container import DregsContainer
from exceptions import CoffeeMachineException
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

    def prepare(self, program):
        coffee_program = self.coffee_programs.get(program)
        if coffee_program is None:
            raise CoffeeMachineException(
                "{} program has not been found. Most probably it has not been programmed.".format(program))
        """
        - coffee program has information about a) order of ingredients; b) amount of each ingredient
        - each ingredient requires a component linked with CoffeeMachine
            * coffee - grinder, dregs_container
            * milk - milk_pump
            * water - water_supply
                grinded_coffee = self.grinder.get_coffee(coffee_ingredient.amount / 2, num_espresso_units)  # espresso ratio 1 g coffee : 2 ml of water
                water = self.water_supply.get_water(coffee_ingredient.amount)
                self.extract_coffee(grinded_coffee, water)
                self.dregs_container.store(grinded_coffee)
                ###
                milk = self.milk_pump.get_milk(milk_ingredient.amount)
                self.add_coffee(milk)
                ###
                water = self.water_supply.get_water(water_ingredient.amount)
                self.add_water(water)
        - 
        """

    def is_ready(self):
        return all(
            (isinstance(self.grinder, CoffeeGrinder),
             isinstance(self.water_supply, WaterSupply),
             isinstance(self.dregs, DregsContainer))
        )
