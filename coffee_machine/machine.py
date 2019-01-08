from inspect import getmembers, isclass, isabstract

from coffee_machine import coffees
from coffee_machine.components import (Brewer, CoffeeGrinder, DregsContainer,
                                       MilkPump, WaterTank)
from coffee_machine.config import get_params


class CoffeeMachine(object):

    def __init__(self, water_supply=WaterTank):
        params = get_params()
        __version__ = params['CoffeeMachine']['version']
        __model__ = params['CoffeeMachine']['model']

        self.water_supply = water_supply(self)
        self.dregs = DregsContainer(self)
        self.grinder = CoffeeGrinder(self)
        self.brewer = Brewer(self)
        self.milk_pump = MilkPump(self)
        self.components = {self.grinder, self.water_supply, self.dregs,
                           self.brewer, self.milk_pump}
        self.notifications = {}

        self.is_ready()
        self.coffee_programs = {}  # TODO: add typing - key: str, val: class
        self._load_coffee_programs()

        self.procedure_steps = {
            coffees.Coffee: self.add_coffee,
            coffees.Milk: self.add_milk,
        }

    def _load_coffee_programs(self):
        classes = getmembers(coffees,
                             lambda c: isclass(c) and not isabstract(c))
        for name, klass in classes:
            if isclass(klass) and issubclass(klass, coffees.AbcCoffeeProgram):
                self.coffee_programs.update({name: klass})

    def supply_milk(self):
        self.milk_pump.supply_milk()

    def prepare(self, program, add_espresso=False):
        coffee_program = self.coffee_programs.get(program)
        if coffee_program is None:
            raise KeyError(
                '"{}" program has not been found. Most probably it has not been programmed.'.format(program))
        c = coffee_program()
        if add_espresso:
            c.coffee.units += 1
        for ingredient in c.follow_procedure():
            self.procedure_step(ingredient)
            pass

    def procedure_step(self, ingredient):
        try:
            step = self.procedure_steps[type(ingredient)]
        except KeyError as e:
            raise TypeError('Coffee machine {} does not know what to do with {}'.format(self, ingredient)) from e
        else:
            step(ingredient)

    def add_coffee(self, coffee: coffees.Coffee):
        grinded_coffee = self.grinder.grind(coffee.grains_amount)
        water = self.water_supply.get_water(coffee.water_amount)
        self.brewer.extract_coffee(grinded_coffee, water)
        self.dregs.store(grinded_coffee)

    def add_milk(self, milk: coffees.Milk):
        milk = self.milk_pump.get_milk(milk.amount)

    def is_ready(self):
        return all(c.health() for c in self.components)
