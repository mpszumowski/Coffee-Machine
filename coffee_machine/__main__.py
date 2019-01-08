from coffee_machine.machine import CoffeeMachine


def start():
    machine = CoffeeMachine()
    running = True

    programs = machine.coffee_programs
    # TODO: add standby phase to catch first KeyboardInterrupt
    # TODO: add readiness checks and refill/empty commands

    while running:

        while machine.ready:

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

        for _, message in machine.notifications.items():
            print(message)

        operations = {
            'refill water': machine.water_supply.refill,
            'empty dregs': machine.dregs.empty,
            'refill coffee': machine.grinder.refill,
            'supply milk': machine.milk_pump.supply_milk
        }

        print('Use one of the following commands:')
        for op in operations.keys():
            print(op)

        command = input()

        try:
            operation = operations[command]
        except KeyError:
            print('Unknown command, please try again')
        else:
            operation()
        machine.is_ready()  # TODO: move this check to internal machine logic


start()
