from inspect import getmembers, isclass, isabstract

import coffees
from config import get_params, get_config
from dregs_container import DregsContainer
from exceptions import CoffeeMachineException
from water_supply import WaterSupply


class CoffeeGrinder(object):

    def __init__(self):
        config = get_config()
        params = get_params()
        self.warning_level = config['CoffeeGrinder']['warning_level']
        self.capacity = params['CoffeeGrinder']['size']
        self._level = 0

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


class Brewer(object):

    @staticmethod
    def extract_coffee(grinded_coffee, water):
        coffee = water
        return coffee


class CoffeeMachine(object):

    def __init__(self, water_supply):
        params = get_params()
        __version__ = params['CoffeeMachine']['version']
        __model__ = params['CoffeeMachine']['model']

        self.water_supply = water_supply()
        self.dregs = DregsContainer()
        self.grinder = CoffeeGrinder()
        self.brewer = Brewer()
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

    def prepare(self, program):
        coffee_program = self.coffee_programs.get(program)
        if coffee_program is None:
            raise CoffeeMachineException(
                '"{}" program has not been found. Most probably it has not been programmed.'.format(program))
        for ingredient in coffee_program.procedure:
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
        grinded_coffee = self.grinder.grind(coffee.grains)
        water = self.water_supply.get_water(coffee.water)
        self.brewer.extract_coffee(grinded_coffee, water)
        self.dregs.store(grinded_coffee)

    def add_milk(self, milk: coffees.Milk):
        pass

    """
    def add_coffee(self, amount, num_espresso_units):
        grinded_coffee = self.grinder.grind(amount / 2, num_espresso_units)  # espresso ratio 1 g coffee : 2 ml of water
        water = self.water_supply.get_water(amount)
        self.brewer.extract_coffee(grinded_coffee, water)
        self.dregs.store(grinded_coffee)

    def add_milk(self, amount):
        milk = self.milk_pump.get_milk(amount)
        self.add_coffee(milk)

    def add_water(self, amount):
        water = self.water_supply.get_water(amount)
        self.add_water(water)
    """

    def is_ready(self):
        return all(
            (isinstance(self.grinder, CoffeeGrinder),
             isinstance(self.water_supply, WaterSupply),
             isinstance(self.dregs, DregsContainer),
             isinstance(self.brewer, Brewer))
        )
