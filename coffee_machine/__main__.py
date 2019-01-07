from coffee_machine.machine import CoffeeMachine


def start(water_supply):
    machine = CoffeeMachine(water_supply)
    running = True

    programs = machine.coffee_programs

    while running:

        is_ready = machine.is_ready()

        while is_ready:

            command = input()

            try:
                program = programs[command]
            except KeyError:
                print('There is no such coffee program.')
            else:
                machine.prepare(program)

start()
