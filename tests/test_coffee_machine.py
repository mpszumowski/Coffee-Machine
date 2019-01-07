import unittest

from coffee_machine.machine import CoffeeMachine
from coffee_machine.components import WaterLine


class TestInitialization(unittest.TestCase):

    def test_initialization(self):
        machine = CoffeeMachine()

    def test_init_waterline(self):
        machine = CoffeeMachine(water_supply=WaterLine)


if __name__ == '__main__':
    unittest.main()
