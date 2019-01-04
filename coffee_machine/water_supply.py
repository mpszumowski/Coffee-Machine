from abc import ABCMeta

from coffee_machine.config import get_config
from coffee_machine.exceptions import WaterTankException


class WaterSupply(metaclass=ABCMeta):

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
