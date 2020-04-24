import tools


while(True):
    tools.print_screen()
    try:
        tools.modes[int(input('Please choose your action: '))]()
    except KeyError:
        print('\nCommand not available!')
    except ValueError:
        print('\nThat\'s not a number...')
    except KeyboardInterrupt:
        print('\nPlease, only do keyboard interrupts if strictly necessary. I may break :(')
        tools.reset(False)
    print('\n')
