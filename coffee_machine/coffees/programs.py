from .abc_coffee import AbcCoffeeProgram
from .ingredients import Coffee, Milk


class Cappuccino(AbcCoffeeProgram):
    _coffee = Coffee(units=1)
    _milk = Milk(60)
    _procedure = ('coffee', 'milk')


class Doppio(AbcCoffeeProgram):
    _coffee = Coffee(units=2)
    _procedure = ('coffee',)


class Espresso(AbcCoffeeProgram):
    _coffee = Coffee(units=1)
    _procedure = ('coffee',)


class Latte(AbcCoffeeProgram):
    _coffee = Coffee(units=1)
    _milk = Milk(220)
    _procedure = ('milk', 'coffee')


class Lungo(AbcCoffeeProgram):
    _coffee = Coffee(units=1, additional_water=90)
    _procedure = ('coffee',)


class Macchiato(AbcCoffeeProgram):
    _coffee = Coffee(units=1)
    _milk = Milk(30)
    _procedure = ('coffee', 'milk')
