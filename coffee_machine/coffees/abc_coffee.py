from abc import ABCMeta, abstractmethod
from copy import copy


class AbcCoffeeProgram(metaclass=ABCMeta):

    def __init__(self):
        self.coffee = copy(self._coffee)
        self.milk = copy(self._milk)

    @property
    @abstractmethod
    def _coffee(self):
        pass

    @property
    def _milk(self):
        return 0

    @property
    @abstractmethod
    def _procedure(self):
        pass

    def follow_procedure(self):
        for ingredient in self._procedure:
            yield getattr(self, ingredient)
