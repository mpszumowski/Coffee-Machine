from abc import ABCMeta, abstractmethod

from coffee_machine.config import get_config, get_params
from coffee_machine.exceptions import WaterTankException, DregsContainerException


class CoffeeMachineComponent(metaclass=ABCMeta):

    def __init__(self, owner, *args, **kwargs):
        self.owner = owner
        super(CoffeeMachineComponent, self).__init__(*args, **kwargs)

    @abstractmethod
    def health(self):
        pass

    def notify(self, message=None):
        info_key = type(self).__name__
        if not message:
            self.owner.notifications.pop(info_key, None)
        else:
            notification = '{} \n {}'.format(str(self), message)
            self.owner.notifications.update({info_key: notification})


class WaterSupply(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Water supply connected...')

    @abstractmethod
    def get_water(self, amount):
        """Return amount passed and do optional things"""


class RefillableContainer(object):

    def __init__(self, *args, **kwargs):
        self._level = 0
        super(RefillableContainer, self).__init__(*args, **kwargs)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, amount):
        if amount < 0:
            raise ValueError('Level of Refillable Container subclass: '
                             '{} cannot be lower than 0'.format(self.__class__))
        self._level = amount

    def add(self, amount):
        self.level += amount

    def subtract(self, amount):
        self.level -= amount


class WaterLine(WaterSupply, CoffeeMachineComponent):

    def __str__(self):
        return "Water line supply"

    def get_water(self, amount):
        return amount

    def health(self):
        return True


class WaterTank(RefillableContainer, WaterSupply, CoffeeMachineComponent):

    def __init__(self, owner):
        super().__init__(owner)
        config = get_config()
        params = get_params()
        self.warning_level = config['WaterTank']['warning_level']
        self.volume = params['WaterTank']['size']

    def __str__(self):
        return 'Water tank component. Volume: {} | Current level: {}'.format(
            self.volume, self.level
        )

    @RefillableContainer.level.setter
    def level(self, amount):
        RefillableContainer.level.fset(self, amount)
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

    def health(self):
        is_ready = self.is_ready()
        message = None
        if not is_ready:
            message = 'Water low: refill water tank'
        self.notify(message=message)
        return is_ready

    def is_ready(self):
        return self.level > self.volume * self.warning_level


class CoffeeGrinder(RefillableContainer, CoffeeMachineComponent):

    def __init__(self, owner):
        super().__init__(owner)
        config = get_config()
        params = get_params()
        self.warning_level = config['CoffeeGrinder']['warning_level']
        self.capacity = params['CoffeeGrinder']['size']
        print('Coffee grinder is up...')

    def __str__(self):
        return 'Coffee Grinder component. Capacity: {} | Current level: {}'.format(
            self.capacity, self.level
        )

    def refill(self, amount):
        super().add(amount)

    def grind(self, amount):
        super().subtract(amount)
        return amount

    def health(self):
        is_ready = self.is_ready()
        message = None
        if not is_ready:
            message = 'Coffee low: refill coffee grinder'
        self.notify(message=message)
        return is_ready

    def is_ready(self):
        return self.level > self.capacity * self.warning_level


class DregsContainer(RefillableContainer, CoffeeMachineComponent):

    def __init__(self, owner):
        super().__init__(owner)
        config = get_config()
        params = get_params()
        self.warning_level = config['DregsContainer']['warning_level']
        self.max_volume = params['DregsContainer']['size']
        self._level = 0
        print('Dregs container connected...')

    def __str__(self):
        return 'Dregs container component. Capacity: {} | Current level: {}'.format(
            self.max_volume, self.level
        )

    @RefillableContainer.level.setter
    def level(self, amount):
        if amount > self.max_volume:
            raise DregsContainerException("Dregs container is full!")
        RefillableContainer.level.fset(self, amount)
        if not self.is_ready():
            # TODO: notify machine to stop serving coffee
            pass

    def empty(self):
        amount = self.level
        super().subtract(amount)

    def store(self, amount):
        super().add(amount)

    def health(self):
        is_ready = self.is_ready()
        message = None
        if not is_ready:
            message = 'Dregs container full: empty container'
        self.notify(message=message)
        return is_ready

    def is_ready(self):
        return self.level < self.max_volume * self.warning_level


class Brewer(CoffeeMachineComponent):

    def __init__(self, owner):
        super().__init__(owner)
        print('Brewer is up...')

    def __str__(self):
        return 'Brewer component'

    @staticmethod
    def extract_coffee(grinded_coffee_amount, water_amount):
        """This method symbolises coffee extraction"""
        coffee = water_amount
        return coffee

    def health(self):
        self.notify()
        return self.is_ready()

    def is_ready(self):
        return True


class MilkPump(CoffeeMachineComponent):

    def __init__(self, owner):
        super().__init__(owner)
        self.milk_supply = None
        print('Milk pump is ready...')

    def __str__(self):
        return 'Milk pump component'

    def supply_milk(self):
        self.milk_supply = True

    def get_milk(self, milk_amount):
        """Symbolic milk getter. In most coffee machines, the milk pump does not know if you supply milk.
        It either pumps it or returns nothing."""
        milk = 0
        if self.milk_supply:
            milk = milk_amount
        return milk

    def health(self):
        self.notify()
        return self.is_ready()

    def is_ready(self):
        return True
