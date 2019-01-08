import unittest

from coffee_machine.machine import CoffeeMachine


class TestInitialization(unittest.TestCase):

    def test_initialization(self):
        machine = CoffeeMachine()


if __name__ == '__main__':
    unittest.main()
