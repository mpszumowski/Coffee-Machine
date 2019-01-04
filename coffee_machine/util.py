from inspect import getmembers, isclass, isabstract
from coffee_machine import coffees


def get_coffee_programs():
    """
    Yield tuples of class (name, type) representing coffee programs from coffees package
    """
    classes = getmembers(coffees,
                         lambda c: isclass(c) and not isabstract(c))
    for name, klass in classes:
        if isclass(klass) and issubclass(klass, coffees.AbcCoffeeProgram):
            yield name, klass
