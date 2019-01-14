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


if __name__ == '__main__':
    unittest.main()
