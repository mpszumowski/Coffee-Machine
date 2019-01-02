from abc import ABCMeta, abstractmethod


class AbcCoffee(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    @property
    def coffee_amount(self):
        pass

    @abstractmethod
    @property
    def milk_amount(self):
        pass

    @abstractmethod
    @property
    def water_amount(self):
        pass
