from .abc_coffee import AbcCoffeeProgram


class Cappuccino(AbcCoffeeProgram):
    coffee_amount = 30
    milk_amount = 60


class Doppio(AbcCoffeeProgram):
    coffee_amount = 60


class Espresso(AbcCoffeeProgram):
    coffee_amount = 30


class Latte(AbcCoffeeProgram):
    coffee_amount = 30
    milk_amount = 220


class Lungo(AbcCoffeeProgram):
    coffee_amount = 30
    water_amount = 120


class Macchiato(AbcCoffeeProgram):
    coffee_amount = 30
    milk_amount = 30
