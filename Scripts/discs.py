from itertools import combinations
import disc_setup

print('-------------------------------------------')
print(' All units are designed to be in KILOGRAMS')
print('-------------------------------------------')
print()


#weight_dict = setup()

while(True):
    disc_setup.print_screen()
    try:
        disc_setup.modes[int(input('Please choose your action: '))]()
    except KeyError:
        print('Command not available!')
    except ValueError:
        print('Invalid operation.')
    except KeyboardInterrupt:
        pass
