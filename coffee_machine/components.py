from abc import ABCMeta

from coffee_machine.config import get_config, get_params
from coffee_machine.exceptions import WaterTankException, DregsContainerException


class RefillableContainer(object):
    pass


class WaterSupply(metaclass=ABCMeta):

    def __init__(self):
        print('Water supply connected...')

    def get_water(self, amount):
        raise NotImplementedError


class WaterLine(WaterSupply):

    def get_water(self, amount):
        return amount


class WaterTank(WaterSupply):

    def __init__(self, volume):
        config = get_config()
        self.warning_level = config['WaterTank']['warning_level']
        self.volume = volume
        self._level = 0
        super().__init__()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, amount):
        self._level = amount
        if self._level < self.volume * self.warning_level:
            #  TODO: notify user to refill water tank
            pass

    def refill(self, amount):
        self._level += amount

    def get_water(self, amount):
        if self._level < amount:
            raise WaterTankException("The water tank is empty!")
        self._level -= amount
        return amount


class DregsContainer(object):

    def __init__(self):
        config = get_config()
        params = get_params()
        self.warning_level = config['DregsContainer']['warning_level']
        self.error_level = params['DregsContainer']['error_level']
        self.max_volume = params['DregsContainer']['size']
        self._level = 0
        print('Dregs container connected...')

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if value > self.max_volume:
            raise DregsContainerException("Dregs container is full!")
        self._level = value
        if self._level > self.max_volume * self.error_level:
            # TODO: notify machine to stop serving coffee
            pass
        elif self._level > self.max_volume * self.warning_level:
            # TODO: notify user to empty dregs container
            pass

    def store(self, value):
        self.level += value


class CoffeeGrinder(object):

    def __init__(self):
        config = get_config()
        params = get_params()
        self.warning_level = config['CoffeeGrinder']['warning_level']
        self.capacity = params['CoffeeGrinder']['size']
        self._level = 0
        print('Coffee grinder is up...')

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

    def __init__(self):
        print('Brewer is up...')

    @staticmethod
    def extract_coffee(grinded_coffee_amount, water_amount):
        """This method symbolises coffee extraction"""
        coffee = water_amount
        return coffee


class MilkPump(object):

    def __init__(self):
        self.milk_supply = None
        print('Milk pump is ready...')

    def supply_milk(self):
        self.milk_supply = True

    def get_milk(self, milk_amount):
        """Symbolic milk getter. In most coffee machines, the milk pump does not know if you supply milk.
        It either pumps it or returns nothing."""
        milk = 0
        if self.milk_supply:
            milk = milk_amount
        return milk
