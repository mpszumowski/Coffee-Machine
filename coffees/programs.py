from .abc_coffee import AbcCoffeeProgram
from .ingredients import Coffee, Milk


class Cappuccino(AbcCoffeeProgram):
    coffee = Coffee(units=1)
    milk = Milk(60)
    

class Doppio(AbcCoffeeProgram):
    coffee = Coffee(units=2)


class Espresso(AbcCoffeeProgram):
    coffee = Coffee(units=1)


class Latte(AbcCoffeeProgram):
    coffee = Coffee(units=1)
    milk = Milk(220)


class Lungo(AbcCoffeeProgram):
    coffee = Coffee(units=1, additional_water=90)


class Macchiato(AbcCoffeeProgram):
    coffee = Coffee(units=1)
    milk = Milk(30)
