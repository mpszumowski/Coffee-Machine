from coffee_machine.machine import CoffeeMachine


def start():
    machine = CoffeeMachine()
    running = True

    programs = machine.coffee_programs

    while running:

        is_ready = machine.is_ready()

        while is_ready:

            print('Select program:')
            for key in programs.keys():
                print(key)

            program = input()
            try:
                machine.prepare(program)
            except KeyError as e:
                print(e)


start()
