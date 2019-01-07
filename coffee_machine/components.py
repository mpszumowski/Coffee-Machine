from abc import ABCMeta, abstractmethod

from coffee_machine.config import get_config, get_params
from coffee_machine.exceptions import WaterTankException, DregsContainerException


class CoffeeMachineComponent(metaclass=ABCMeta):

    @abstractmethod
    def is_ready(self) -> bool:
        pass


class RefillableContainer(object):

    def __init__(self):
        self._level = 0
        super(RefillableContainer, self).__init__()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, amount):
        self._level = amount

    def add(self, amount):
        self.level += amount

    def subtract(self, amount):
        self.level -= amount


class CoffeeGrinder(RefillableContainer, CoffeeMachineComponent):

    def __init__(self):
        super().__init__()
        config = get_config()
        params = get_params()
        self.warning_level = config['CoffeeGrinder']['warning_level']
        self.capacity = params['CoffeeGrinder']['size']
        print('Coffee grinder is up...')

    def refill(self, amount):
        super().add(amount)

    def grind(self, amount):
        super().subtract(amount)
        return amount

    def is_ready(self):
        return self.level < self.capacity * self.warning_level


class WaterSupply(metaclass=ABCMeta):

    def __init__(self):
        print('Water supply connected...')

    @abstractmethod
    def get_water(self, amount):
        """Return amount passed and do optional things"""


class WaterLine(WaterSupply, CoffeeMachineComponent):

    def get_water(self, amount):
        return amount

    def is_ready(self):
        return True


class WaterTank(RefillableContainer, WaterSupply):

    def __init__(self):
        super().__init__()
        config = get_config()
        params = get_params()
        self.warning_level = config['WaterTank']['warning_level']
        self.volume = params['WaterTank']['size']

    @RefillableContainer.level.setter
    def level(self, amount):
        self._level = amount
        print('Setting watertank level')
        if not self.is_ready():
            #  TODO: notify user to refill water tank
            pass

    def refill(self, amount):
        super().add(amount)

    def get_water(self, amount):
        if self.level < amount:
            raise WaterTankException("The water tank is empty!")
        super().subtract(amount)
        return amount

    def is_ready(self):
        return self.level < self.volume * self.warning_level


class DregsContainer(RefillableContainer, CoffeeMachineComponent):

    def __init__(self):
        super().__init__()
        config = get_config()
        params = get_params()
        self.warning_level = config['DregsContainer']['warning_level']
        self.max_volume = params['DregsContainer']['size']
        self._level = 0
        print('Dregs container connected...')

    @RefillableContainer.level.setter
    def level(self, amount):
        if amount > self.max_volume:
            raise DregsContainerException("Dregs container is full!")
        self._level = amount
        if not self.is_ready():
            # TODO: notify machine to stop serving coffee
            pass

    def store(self, amount):
        super().add(amount)

    def is_ready(self):
        return self.level < self.max_volume * self.warning_level


class Brewer(CoffeeMachineComponent):

    def __init__(self):
        print('Brewer is up...')

    @staticmethod
    def extract_coffee(grinded_coffee_amount, water_amount):
        """This method symbolises coffee extraction"""
        coffee = water_amount
        return coffee

    def is_ready(self):
        return True


class MilkPump(CoffeeMachineComponent):

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

    def is_ready(self):
        return True
