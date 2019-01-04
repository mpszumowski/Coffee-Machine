from coffee_machine.coffee_machine import CoffeeMachine


def start(water_supply):
    machine = CoffeeMachine(water_supply)
    running = True

    programs = machine.coffee_programs

    while running:


        command = input()

start()
