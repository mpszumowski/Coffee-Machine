import unittest
from unittest import mock

from coffee_machine import coffees
from coffee_machine import components
from coffee_machine.machine import CoffeeMachine


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

    def test_prepare_coffee(self):
        for Program in self.m.coffee_programs.values():
            program = Program()
            with self.assertRaises(ValueError):
                self.m.prepare(type(program).__name__)


class TestWaterTankComponent(unittest.TestCase):

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


class TestCoffeeGrinderComponent(unittest.TestCase):

    def setUp(self):
        self.m = CoffeeMachine()

    def test_grinder(self):
        self.assertIsInstance(self.m.grinder, components.CoffeeGrinder)

    def test_grinder_ready(self):
        self.assertFalse(self.m.grinder.is_ready())
        self.m.grinder.refill()
        self.assertTrue(self.m.grinder.is_ready())

    def test_grinder_level(self):
        self.m.grinder.refill()
        with self.assertRaises(ValueError):
            exceeding_amount = self.m.grinder.level + 1
            self.m.grinder.grind(exceeding_amount)

    @mock.patch('coffee_machine.machine.CoffeeMachine')
    def test_grinder_notification(self, mock_coffee_machine):
        self.m.grinder.owner = mock_coffee_machine
        self.m.grinder.grind(self.m.grinder.level)
        self.assertIsNot(self.m.grinder.owner, {})


class TestDregsContainerComponent(unittest.TestCase):

    def setUp(self):
        self.m = CoffeeMachine()

    def test_grinder(self):
        self.assertIsInstance(self.m.dregs, components.DregsContainer)

    def test_grinder_ready(self):
        self.assertTrue(self.m.dregs.is_ready())

    def test_grinder_level(self):
        exceeding_amount = self.m.dregs.volume + 1
        with self.assertRaises(ValueError):
            self.m.dregs.store(exceeding_amount)

    @mock.patch('coffee_machine.machine.CoffeeMachine')
    def test_grinder_notification(self, mock_coffee_machine):
        self.m.dregs.owner = mock_coffee_machine
        self.m.dregs.store(self.m.dregs.level)
        self.assertIsNot(self.m.dregs.owner, {})


class TestBrewer(unittest.TestCase):

    def setUp(self):
        self.m = CoffeeMachine()

    def test_brewer_ready(self):
        self.assertTrue(self.m.brewer.is_ready())

    def test_brewer_extraction(self):
        coffee_amount = 30
        water_amount = 60
        self.assertEqual(self.m.brewer.extract_coffee(coffee_amount, water_amount), water_amount)


class TestMilkPump(unittest.TestCase):

    def setUp(self):
        self.m = CoffeeMachine()

    def test_milk_supply_ready(self):
        self.assertFalse(self.m.milk_pump.is_ready())
        self.m.milk_pump.supply_milk()
        self.assertTrue(self.m.milk_pump.is_ready())

    def test_get_milk(self):
        milk = 60
        self.m.milk_pump.supply_milk()
        self.assertEqual(self.m.milk_pump.get_milk(milk), milk)


if __name__ == '__main__':
    unittest.main()
