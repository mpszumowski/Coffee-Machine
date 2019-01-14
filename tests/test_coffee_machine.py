import unittest
from unittest import mock
from inspect import getmembers, isclass, isabstract

from coffee_machine.machine import CoffeeMachine
from coffee_machine import components
from coffee_machine import coffees


class TestInitialization(unittest.TestCase):

    def test_initialization(self):
        machine = CoffeeMachine()


class TestPrograms(unittest.TestCase):

    def setUp(self):
        self.m = CoffeeMachine()

    def test_loading(self):
        self.assertIsNot(self.m.coffee_programs, {})

    def test_coffee(self):
        for Program in self.m.coffee_programs.values():
            program = Program()
            self.assertIsInstance(program._coffee, coffees.ingredients.Coffee)


class TestComponents(unittest.TestCase):

    def setUp(self):
        self.m = CoffeeMachine()

    def test_water_tank(self):
        self.assertIsInstance(self.m.water_supply, components.WaterTank)

    def test_water_tank_ready(self):
        self.assertFalse(self.m.water_supply.is_ready())
        self.m.water_supply.refill()
        self.assertTrue(self.m.water_supply.is_ready())

    def test_water_tank_level(self):
        self.m.water_supply.refill()
        with self.assertRaises(ValueError):
            exceeding_amount = self.m.water_supply.level + 1
            self.m.water_supply.get_water(exceeding_amount)

    @mock.patch('coffee_machine.machine.CoffeeMachine')
    def test_water_tank_notification(self, mock_coffee_machine):
        self.m.water_supply.owner = mock_coffee_machine
        self.m.water_supply.get_water(self.m.water_supply.level)
        self.assertIsNot(self.m.water_supply.owner, {})


if __name__ == '__main__':
    unittest.main()
