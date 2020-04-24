from itertools import combinations

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        if value not in self[key]:
            self[key].append(value)

filename = "data.dat"
bar = 0
d = Dictlist()
file = None

def is_setup():
    try:
        with open(filename) as f:
            return len(f.readline())!=0
    except FileNotFoundError:
        return False

def setup():
    if is_setup():
        check = input('Do you really want to override your previous data? (Y/N) ')
        if not check.upper().startswith('Y'):
            print('I thought so! :)')
            return
        else:
            print('It never hurts to ask! :)\n')
    
    global file
    file = open(filename, "w+")
    valid = False
    while (not valid):
        global bar
        bar = input('How much does your bar weigh? ')
        try:
            bar = float(bar)
            if bar <= 0:
                raise ValueError('Bar weight cannot be negative or zero!');
            valid = True
        except ValueError:
            print("'" + str(bar) + "' is not a valid number.")

    file.write(str(bar)+';\n')
    microplates = input('Do you have microplates? (Y/N) ')
    if microplates.upper().startswith('Y'):
        microplates = True
        print('Program configured WITH microplates')
    else:
        microplates = False
        print('Program configured WITHOUT microplates')

    weights_available = (25, 20, 15, 10, 5, 2.5, 1.25)
    microplates_available = (0.5, 0.75, 1, 1.5, 2)

    print()
    discs = {}

    for plate in weights_available:
        valid = False
        discs[plate] = 0
        while (not valid):
            amount = input('How many PAIRS of ' + str(plate) + 'kg disks do you have? ')
            try:
                amount = int(amount)
                discs[plate] = amount
                valid = True
            except ValueError:
                print("'" + str(amount) + "' is not a valid number.")

    if microplates:
        for plate in microplates_available:
            response = input('Do you have a ' + str(plate) + 'kg microplate ? (Y/N) ')
            if response.upper().startswith('Y'):
                discs[plate] = 1
            else:
                discs[plate] = 0

    disc_list = []

    for k,v in discs.items():
        for i in range(v):
            disc_list.append(k)

    print()

    for i in range(1,len(disc_list)+1):
        discs_per_side = tuple(combinations(disc_list, i))
        for j in discs_per_side:
            if len(j) == 1:
                total_weight = sum(j)*2 + bar
                d[total_weight] = j[0]
                file.write(str(total_weight)+';'+str(j[0])+'\n')
            else:
                d[sum(j)*2 + bar] = j
                file.write(str(total_weight)+';'+str(j)+'\n')
    file.close()

    print('\nSetup finished.')


def print_weights():
    if is_setup():
        print()
        print('-----------------------------------------------')
        print('Total weight  \t | \t Plates on each side')
        print('-----------------------------------------------')
        print(str(bar), 'kg  \t-->\t Just the bar!')
        for k,v in sorted(d.items()):
            print(k, 'kg  \t-->\t', v)
    


modes = {0: lambda: exit(), 1: setup, 2: lambda: print('Please, setup first'), 3: lambda: print('Please, setup first')}

def print_screen():
    if is_setup():
        global modes
        modes = {0: lambda: exit(), 1: setup, 2: print_weights, 3: lambda: print('Sadly, not yet available :(')}
        print('--------------------------------------------------')
        print('--                                              --')
        print('--               BARBELL DISCS TOOLS            --')
        print('--   ----------------------------------------   --')
        print('--   Commands available:                        --')
        print('--                                              --')
        print('--   1: Setup                                   --')
        print('--   2: Display all weight combinations         --')
        print('--   3: Check if a certain weight is available  --')
        print('--                                              --')
        print('--   0: Exit              (Units are in KG)     --')
        print('--------------------------------------------------')
    else:
        print('--------------------------------------------------')
        print('--                                              --')
        print('--               BARBELL DISCS TOOLS            --')
        print('--   ----------------------------------------   --')
        print('--   Commands available:                        --')
        print('--                                              --')
        print('--   1: Setup                                   --')
        print('--   2: (Not available until setup complete)    --')
        print('--   3: (Not available until setup complete)    --')
        print('--                                              --')
        print('--   0: Exit              (Units are in KG)     --')
        print('--------------------------------------------------')

def read_savefile():
    file = open("data.dat", "w+")
