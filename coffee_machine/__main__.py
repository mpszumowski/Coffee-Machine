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
                programs[program]
            except KeyError as e:
                print(e)
            else:
                print('Make it a notch stronger? \n y/n')
                command = input()
                add_espresso = False
                if command.lower()[0] == 'y':
                    print('Sure thing')
                    add_espresso = True
                elif command.lower()[0] == 'n':
                    pass
                else:
                    print('Could not understand you. I\'ll make it stronger, '
                          'but consider a triple.')
                    add_espresso = True
                machine.prepare(program, add_espresso)


start()
