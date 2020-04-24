from itertools import combinations
import tools


while(True):
    tools.print_screen()
    try:
        tools.modes[int(input('Please choose your action: '))]()
    except KeyError:
        print('Command not available!')
    except ValueError:
        print('That\'s not a number...')
    except KeyboardInterrupt:
        print('Please, don\'t be rude and use command \'0\' to exit')
    print('\n')
