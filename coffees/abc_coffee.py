from abc import ABCMeta, abstractmethod


class AbcCoffee(metaclass=ABCMeta):
    @property
    @abstractmethod
    def coffee_amount(self):
        raise NotImplementedError

    @property
    def milk_amount(self):
        return 0

    @property
    def water_amount(self):
        return 0
