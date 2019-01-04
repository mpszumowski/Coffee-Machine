from .abc_coffee import AbcCoffeeProgram
from .ingredients import Coffee, Milk


class Cappuccino(AbcCoffeeProgram):
    coffee = Coffee(units=1)
    milk = Milk(60)
    procedure = (coffee, milk)


class Doppio(AbcCoffeeProgram):
    coffee = Coffee(units=2)
    procedure = (coffee,)


class Espresso(AbcCoffeeProgram):
    coffee = Coffee(units=1)
    procedure = (coffee,)


class Latte(AbcCoffeeProgram):
    coffee = Coffee(units=1)
    milk = Milk(220)
    procedure = (milk, coffee)


class Lungo(AbcCoffeeProgram):
    coffee = Coffee(units=1, additional_water=90)
    procedure = (coffee,)


class Macchiato(AbcCoffeeProgram):
    coffee = Coffee(units=1)
    milk = Milk(30)
    procedure = (coffee, milk)
