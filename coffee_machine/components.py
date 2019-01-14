from abc import ABCMeta, abstractmethod
from functools import wraps

from coffee_machine.config import get_config, get_params
from coffee_machine.exceptions import WaterTankException, DregsContainerException


class CoffeeMachineComponent(metaclass=ABCMeta):

    def __init__(self, owner, *args, **kwargs):
        self.owner = owner  # TODO: typing
        super(CoffeeMachineComponent, self).__init__(*args, **kwargs)

    @property
    @abstractmethod
    def warning_message(self):
        pass

    def health(self):
        is_ready = self.is_ready()
        message = None
        if not is_ready:
            message = self.warning_message
        self._notify(message=message)
        return is_ready

    @abstractmethod
    def is_ready(self):
        pass

    def _notify(self, message=None):
        component_name = type(self).__name__
        if not message:
            self.owner.update(component_name)
        else:
            notification = '{} \n {}'.format(str(self), message)
            self.owner.update(component_name, notification)


class RefillableContainer(object):

    def __init__(self, volume, *args, **kwargs):
        self._level = 0
        self._volume = volume
        super(RefillableContainer, self).__init__(*args, **kwargs)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, amount):
        if amount < 0:
            raise ValueError('Level of Refillable Container subclass: '
                             '{} cannot be lower than 0'.format(self.__class__))
        if amount > self._volume:
            raise ValueError('Level of Refillable Container subclass: '
                             '{} cannot exceed its volume'.format(self.__class__))
        self._level = amount

    @property
    def volume(self):
        return self._volume

    def add(self, amount):
        self.level += amount

    def subtract(self, amount):
        self.level -= amount


class WaterTank(RefillableContainer, CoffeeMachineComponent):

    warning_message = 'Water low: refill water tank'

    def __init__(self, owner):
        config = get_config()
        params = get_params()
        self.warning_level = config['WaterTank']['warning_level']
        volume = params['WaterTank']['size']
        super().__init__(owner=owner, volume=volume)
        print('Water tank connected')

    def __str__(self):
        return 'Water tank component. Volume: {} | Current level: {}'.format(
            self.volume, self.level
        )

    def refill(self):
        amount = self.volume - self.level
        super().add(amount)
        self.health()
        print('Watertank refilled')

    def get_water(self, amount):
        super().subtract(amount)
        self.health()
        return amount

    def is_ready(self):
        return self.level > self.volume * self.warning_level


class CoffeeGrinder(RefillableContainer, CoffeeMachineComponent):

    warning_message = 'Coffee low: refill coffee grinder'

    def __init__(self, owner):
        config = get_config()
        params = get_params()
        self.warning_level = config['CoffeeGrinder']['warning_level']
        volume = params['CoffeeGrinder']['size']
        super().__init__(owner=owner, volume=volume)
        print('Coffee grinder is up...')

    def __str__(self):
        return 'Coffee Grinder component. Capacity: {} | Current level: {}'.format(
            self.volume, self.level
        )

    def refill(self):
        amount = self.volume - self.level
        super().add(amount)
        self.health()
        print('Coffee grinder refilled.')

    def grind(self, amount):
        super().subtract(amount)
        self.health()
        return amount

    def is_ready(self):
        return self.level > self.volume * self.warning_level


class DregsContainer(RefillableContainer, CoffeeMachineComponent):

    warning_message = 'Dregs container full: empty container'

    def __init__(self, owner):
        config = get_config()
        params = get_params()
        self.warning_level = config['DregsContainer']['warning_level']
        volume = params['DregsContainer']['size']
        super().__init__(owner=owner, volume=volume)
        print('Dregs container connected...')

    def __str__(self):
        return 'Dregs container component. Capacity: {} | Current level: {}'.format(
            self.volume, self.level
        )

    def empty(self):
        amount = self.level
        super().subtract(amount)
        self.health()
        print('Dregs container is empty.')

    def store(self, amount):
        super().add(amount)
        self.health()

    def is_ready(self):
        return self.level < self.volume * self.warning_level


class Brewer(CoffeeMachineComponent):

    warning_message = 'Unexpected malfunction'

    def __init__(self, owner):
        super().__init__(owner=owner)
        print('Brewer is up...')

    def __str__(self):
        return 'Brewer component'

    @staticmethod
    def extract_coffee(grinded_coffee_amount, water_amount):
        """This method symbolises coffee extraction"""
        coffee = water_amount
        return coffee

    def health(self):
        self._notify()
        return self.is_ready()

    def is_ready(self):
        return True


class MilkPump(CoffeeMachineComponent):

    warning_message = 'Milk is not supplied'

    def __init__(self, owner):
        super().__init__(owner=owner)
        self.milk_supply = None
        print('Milk pump is ready...')

    def __str__(self):
        return 'Milk pump component'

    def supply_milk(self):
        self.milk_supply = True
        self.health()
        print('Milk supplied.')

    def get_milk(self, milk_amount):
        """Symbolic milk getter. In most coffee machines, the milk pump does not know if you supply milk.
        It either pumps it or returns nothing."""
        milk = 0
        if self.milk_supply:
            milk = milk_amount
        return milk

    def is_ready(self):
        return self.milk_supply
