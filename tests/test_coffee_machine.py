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
        patcher = mock.patch('coffee_machine.machine.CoffeeMachine')
        self.addCleanup(patcher.stop)
        self.mock_coffee_machine = patcher.start()

    def test_water_tank(self):
        water_supply = components.WaterTank(self.mock_coffee_machine.result_value)
        self.assertIsInstance(water_supply, components.WaterTank)

    def test_water_tank_ready(self):
        water_supply = components.WaterTank(self.mock_coffee_machine.result_value)
        self.assertFalse(water_supply.is_ready())
        water_supply.refill()
        self.assertTrue(water_supply.is_ready())

    def test_water_tank_level(self):
        water_supply = components.WaterTank(self.mock_coffee_machine.result_value)
        water_supply.refill()
        with self.assertRaises(ValueError):
            exceeding_amount = water_supply.level + 1
            water_supply.get_water(exceeding_amount)

    def test_water_tank_notification(self):
        water_supply = components.WaterTank(self.mock_coffee_machine.result_value)
        water_supply.owner.notifications = {}
        water_supply.get_water(water_supply.level)
        self.assertIsNot(water_supply.owner.notifications, {})


class TestCoffeeGrinderComponent(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('coffee_machine.machine.CoffeeMachine')
        self.addCleanup(patcher.stop)
        self.mock_coffee_machine = patcher.start()

    def test_grinder(self):
        grinder = components.CoffeeGrinder(self.mock_coffee_machine)
        self.assertIsInstance(grinder, components.CoffeeGrinder)

    def test_grinder_ready(self):
        grinder = components.CoffeeGrinder(self.mock_coffee_machine)
        self.assertFalse(grinder.is_ready())
        grinder.refill()
        self.assertTrue(grinder.is_ready())

    def test_grinder_level(self):
        grinder = components.CoffeeGrinder(self.mock_coffee_machine)
        grinder.refill()
        with self.assertRaises(ValueError):
            exceeding_amount = grinder.level + 1
            grinder.grind(exceeding_amount)

    def test_grinder_notification(self):
        grinder = components.CoffeeGrinder(self.mock_coffee_machine)
        grinder.owner.notifications = {}
        grinder.grind(grinder.level)
        self.assertIsNot(grinder.owner, {})


class TestDregsContainerComponent(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('coffee_machine.machine.CoffeeMachine')
        self.addCleanup(patcher.stop)
        self.mock_coffee_machine = patcher.start()

    def test_grinder(self):
        dregs = components.DregsContainer(self.mock_coffee_machine.result_value)
        self.assertIsInstance(dregs, components.DregsContainer)

    def test_grinder_ready(self):
        dregs = components.DregsContainer(self.mock_coffee_machine.result_value)
        self.assertTrue(dregs.is_ready())

    def test_grinder_level(self):
        dregs = components.DregsContainer(self.mock_coffee_machine.result_value)
        exceeding_amount = dregs.volume + 1
        with self.assertRaises(ValueError):
            dregs.store(exceeding_amount)

    def test_grinder_notification(self):
        dregs = components.DregsContainer(self.mock_coffee_machine.result_value)
        dregs.owner.notifications = {}
        dregs.store(dregs.level)
        self.assertIsNot(dregs.owner, {})


class TestBrewer(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('coffee_machine.machine.CoffeeMachine')
        self.addCleanup(patcher.stop)
        self.mock_coffee_machine = patcher.start()

    def test_brewer_ready(self):
        brewer = components.Brewer(self.mock_coffee_machine.result_value)
        self.assertTrue(brewer.is_ready())

    def test_brewer_extraction(self):
        brewer = components.Brewer(self.mock_coffee_machine.result_value)
        coffee_amount = 30
        water_amount = 60
        self.assertEqual(brewer.extract_coffee(coffee_amount, water_amount), water_amount)


class TestMilkPump(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('coffee_machine.machine.CoffeeMachine')
        self.addCleanup(patcher.stop)
        self.mock_coffee_machine = patcher.start()

    def test_milk_supply_ready(self):
        milk_pump = components.MilkPump(self.mock_coffee_machine)
        self.assertFalse(milk_pump.is_ready())
        milk_pump.supply_milk()
        self.assertTrue(milk_pump.is_ready())

    def test_get_milk(self):
        milk_pump = components.MilkPump(self.mock_coffee_machine)
        milk = 60
        milk_pump.supply_milk()
        self.assertEqual(milk_pump.get_milk(milk), milk)


if __name__ == '__main__':
    unittest.main()
