from coffee_machine.coffee_machine import CoffeeMachine
from coffee_machine.util import get_coffee_programs


def start(water_supply):
    machine = CoffeeMachine(water_supply)
    running = True

    programs = {name: klass for name, klass in get_coffee_programs()}

    while running:


        command = input()

start()
