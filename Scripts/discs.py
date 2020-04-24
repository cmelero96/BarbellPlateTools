from itertools import combinations
import tools

while(True):
    tools.print_screen()
    try:
        tools.modes[int(input('Please choose your action: '))]()
    except KeyError:
        print('Command not available!')
    except ValueError:
        print('Invalid operation.')
    except KeyboardInterrupt:
        pass
