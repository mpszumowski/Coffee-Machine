from abc import ABCMeta, abstractmethod


class AbcCoffeeProgram(metaclass=ABCMeta):
    @property
    @abstractmethod
    def coffee(self):
        raise NotImplementedError

    @property
    def milk(self):
        return 0
