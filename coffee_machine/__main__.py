import random
import sys

from coffee_machine.machine import CoffeeMachine


def start():
    machine = CoffeeMachine()
    standby = True
    running = False

    programs = machine.coffee_programs

    normal_responses = [
        "Yes sir?", "Orders Cap'n'?", "I read you.", "Reportin' for duty"
    ]
    additional_responses = [
        "Come again, Cap'n'?", "I'm not readin' you clearly.",
        "You ain't from around here, are you?",
        "I can't believe they put me in one of these things!",
        "And now I gotta put up with this too?",
        "I told 'em I was claustrophobic, I gotta get outta here!",
        "I'm locked in here tighter than a frog's butt in a watermelon seed fight."
    ]

    def gen_additional_resps():
        for resp in additional_responses:
            yield resp

    count = 0
    additional_resps = gen_additional_resps()

    while standby:

        try:
            print('Standby. Type "start"')

            command = input()

            if command == 'start':
                running = True
            elif count < 5:
                print(random.choice(normal_responses))
                count += 1
            else:
                try:
                    print(next(additional_resps))
                except StopIteration:
                    print(random.choice(normal_responses))
                    count = 0
                    additional_resps = gen_additional_resps()
        except KeyboardInterrupt:
            print('Shutting down...')
            sys.exit(0)

        while running:

            try:

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
                        if command and command.lower()[0] == 'y':
                            print('Sure thing')
                            add_espresso = True
                        elif command and command.lower()[0] == 'n':
                            pass
                        else:
                            print('Could not understand you. '
                                  'I\'ll make it stronger, '
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

            except KeyboardInterrupt:
                running = False
                break


start()
