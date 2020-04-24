import itertools
import disc_const

bar_weight = 0
disc_list = []
weights = set()
weights_aux = []
unit = 'kg'
inactive_unit = 'lb'
plates_set = disc_const.plates_kg
microplates_set = disc_const.micro_kg
            
def save():
    print('Saving your data to local file...')
    with open(disc_const.filename, 'w+') as file:
        file.write(disc_const.bar_str + ':' + str(bar_weight) + '\n')
        file.write(disc_const.discs_str + ':' + str(disc_list) + '\n')
        file.write(disc_const.weights_str + ':' + str(weights) + '\n')
        file.write(disc_const.aux_str + ':' + str(weights_aux) + '\n')
    print('  Done!')

def load():
    data = 0
    try:
        with open(disc_const.filename) as file:
            print('Loading information from previous savefile...')
            from ast import literal_eval
            for line in file:
                fields = line.strip().split(":")
                if fields[0] == disc_const.bar_str:
                    print('  Loading bar weight data...')
                    global bar_weight
                    bar_weight = literal_eval(fields[1])
                    data += 1
                elif fields[0] == disc_const.discs_str:
                    print('  Loading available disks data...')
                    global disc_list
                    disc_list = literal_eval(fields[1])
                    data += 1
                elif fields[0] == disc_const.weights_str:
                    print('  Loading weight options data...')
                    global weights
                    if fields[1] == "set()":
                        weights = set()
                    else:
                        weights = literal_eval(fields[1])
                    data += 1
                elif fields[0] == disc_const.aux_str:
                    print('  Loading extra data...')
                    global weights_aux
                    weights_aux = literal_eval(fields[1])
                    data += 1

        if data != 4:
            raise ValueError
        print('  Done!')
        return True
    except ValueError:
        print('  Data file corrupt. Unable to load data.')
        return False
    except FileNotFoundError:
        return False

def reset(show_prompt = True):
    if show_prompt:
        check = input('Are you sure you want to erase all data? (Y/N) ')
        if not check.upper().startswith('Y'):
            print('Well thought :)')
            return
    
    global bar_weight
    bar_weight = 0
    global disc_list
    disc_list = []
    global weights
    weights = set()
    global weights_aux
    weights_aux = []
    try:
        from os import remove
        remove(disc_const.filename)
    except FileNotFoundError:
        pass

    if show_prompt:
        print('All data erased!')


def is_setup():
    if bar_weight != 0:
        return True
    
    return load()

def calc_plates(target):
    options = []
    side_target = (target-bar_weight)/2
    for i in weights_aux:
        
        if sum(i) == side_target:
            options.append(i)

    return sorted(options)[-1]

def print_target(target, w):
    print('|nTarget: ' + str(target) + unit + '. Put on each side:')
    for i in w:
        print('  ' + str(i) + unit + ' plate')

    
def print_weights():
    print('\nThese are the weights you can do with your current equipment:')
    for i in weights:
        print('  ' + str(i) + unit + '')
    print('  ' + str(bar_weight) + unit + ' (this is just the bar)')
    print('Now you can use command #3 to see how to load your desired weight!')
    

def setup():
    if is_setup():
        check = input('Do you really want to override your previous data? (Y/N) ')
        if not check.upper().startswith('Y'):
            print('I thought so! :)')
            return
        else:
            print('It never hurts to ask! :)\n')
            reset(False)

    print()
    print('----- Let\'s start! -----')
    print()
        
    valid = False
    while (not valid):
        global bar_weight
        bar_weight = input('How much does your bar weigh? ')
        try:
            bar_weight = float(bar_weight)
            if bar_weight <= 0:
                raise ValueError('Bar weight cannot be negative or zero!');
            valid = True
        except ValueError:
            print("'" + str(bar_weight) + "' is not a valid number.")

    for plate in plates_set:
            valid = False
            while (not valid):
                amount = input('  How many PAIRS of ' + str(plate) + unit + ' disks do you have? ')
                try:
                    for i in range(int(amount)):
                        disc_list.append(plate)
                    valid = True
                except ValueError:
                    print("'" + str(amount) + "' is not a valid number.")

    microplates = input('Do you have microplates? (Y/N) ')
    if microplates.upper().startswith('Y'):
        for plate in microplates_set:
            response = input('  Do you have a ' + str(plate) + unit + ' microplate? (Y/N) ')
            if response.upper().startswith('Y'):
                disc_list.append(plate)

    if len(disc_list) == 0:
        print('Seems you only have an empty bar!')

    global weights_aux
    for i in range(1,len(disc_list)+1):
        weights_aux += set(itertools.combinations(disc_list, i))

    global weights
    for i in weights_aux:
        weights.add(2*sum(i)+bar_weight)

    weights = sorted(weights, reverse=True)

    save()
    print('Setup complete!')


def print_plates():
    target = input('Select the weight you\'re aiming for: ')
    try:
        target = float(target)
        if target <= 0:
            raise ValueError('Target weight cannot be negative or zero!');
        valid = True
    except ValueError:
        print("'" + str(target) + "' is not a valid number.")

    if target == bar_weight:
        print('Hey, that\'s just the bar!')
    elif target < bar_weight:
        print('No kidding, that\'s less weight than the bar. Try breaking it to pieces...')
    elif target in weights:
        w = calc_plates(target)
        print_target(target, w)
    else:
        abs_difference = lambda weight : abs(weight - target)
        closest_value = min(weights, key=abs_difference)
        w1 = calc_plates(closest_value)
        try:
            second_value = weights[weights.index(closest_value)+1]
            w2 = calc_plates(second_value)
            print('Impossible to hit ' + str(target) + unit + '; here are the two closest options:')
            print_target(closest_value, w1)
            print_target(second_value, w2)
        except IndexError:
            print('Impossible to hit ' + str(target) + unit + '; here is the closest option:')
            print_target(closest_value, w1)


def toggle_units():
    reset(False);
    global unit
    global inactive_unit
    global plates_set
    global microplates_set
    unit, inactive_unit = inactive_unit, unit
    if unit == 'kg':
        plates_set = disc_const.plates_kg
        microplates_set = disc_const.micro_kg
    else:
        plates_set = disc_const.plates_lb
        microplates_set = disc_const.micro_lb

    
def close_program():
    from time import sleep
    print('GOODBYE! :)')
    sleep(1)
    from sys import exit
    exit(0)


modes = {1: setup,
         2: print_weights,
         3: print_plates,
         9: reset,
         8: toggle_units,
         0: close_program}

def print_screen():
    actions_list = {
        1: 'Setup',
        2: 'Display all weight combinations',
        3: 'How to load a certain weight',
        8: 'Change units to ' + inactive_unit + ' (requires reset)',
        9: 'Delete all data'}
    
    global modes
    if is_setup():
        modes[2] = print_weights
        modes[3] = print_plates
        modes[9] = reset
    else:
        modes.pop(2,None)
        modes.pop(3,None)
        modes.pop(9,None)
        actions_list.pop(2,None)
        actions_list.pop(3,None)
        actions_list.pop(9,None)
        
    print('--------------------------------------------------')
    print('--                                              --')
    print('--               BARBELL DISCS TOOLS            --')
    print('--   ----------------------------------------   --')
    print('--   Commands available:                        --')
    print('--                                              --')
    for i in actions_list:
        if i != 0:
            print('--   ' + (str(i) + ": " + actions_list[i]).ljust(43) + '--')
    print('--                                              --')
    print('--   0: Exit                                    --')
    print('--                                              --')
    print('--                  (Currently using ' + unit + ' units)  --')
    print('--------------------------------------------------')
