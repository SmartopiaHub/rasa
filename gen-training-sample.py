import random
from string import Template
from ruamel.yaml import YAML

# define places inside/outside a house

rooms = ['bedroom', 'master room', 'bashroom', 'washroom', 'kitchen', 'laundry room',
         'dining room', 'foyer', 'living room', 'study room', 'balcony', 'shower room',
         'box room', 'play room', 'toilet', 'multimedia room', 'media room', 'home office',
         'library', 'game room', 'sunroom', 'drawing room', 'ballroom', 'nursery',
         'theatre', 'cinema', 'storage', 'storeroom']

floors = ['basement', 'ground floor', 'first floor', 'second floor', 'third floor',
          'fourth floor', 'fifth floor', 'top floor']

spots = ['attic', 'loft', 'porch', 'garage', 'yard', 
         'front yard', 'backyard', 'corridor', 'hallway']

# deivce types
yaml = YAML(typ='safe') 
with open('device-types.yml') as stream:
    dev = yaml.load(stream)

# define asking prefix

ask_prefix = ['could you', 'may you', 'can you', 'would you']


def flip_coin():
    return random.randint(0,1) == 0

def add_room(s):
    if flip_coin(): # add room?
        if flip_coin():
            s = s + ' in ' + make_entity(rooms[random.randint(0,len(rooms)-1)], 'room')
        else:
            s = s + ' in the ' + make_entity(rooms[random.randint(0,len(rooms)-1)], 'room')
    return s

def add_floor(s):
    if flip_coin(): # add floor?
        if flip_coin():
            s = s + ' in ' + make_entity(floors[random.randint(0,len(floors)-1)],'floor')
        else:
            s = s + ' in the ' + make_entity(floors[random.randint(0,len(floors)-1)],'floor')
    return s

def add_ask(s):
    if flip_coin(): # add asking?
        if flip_coin(): # add please?
            if flip_coin(): # add to the end?
                s = ask_prefix[random.randint(0,len(ask_prefix)-1)] + " " + s + " please"
            else:
                s = ask_prefix[random.randint(0,len(ask_prefix)-1)] + " please " + s
        else:
            s = ask_prefix[random.randint(0,len(ask_prefix)-1)] + " " + s
    else:
        if flip_coin(): # add please?
            if flip_coin(): # add to the end?
                s = s + " please"
            else:
                s = "please " + s
    return s

def make_entity(s, ent):
    return '[' + s + '](' + ent + ')'


# intent: change_color

change_color_verb_list = ['change', 'switch', 'convert', 'swap', 'turn']
make_color_verb_list = ['make']
change_color_cmd_list = ['$verb $obj to $color', '$verb color of $obj to $color']
make_color_cmd_list = ['$verb $obj $color', '$verb color of $obj $color']
color_list = ['pink', 'crimson', 'red', 'maroon', 'brown', 'misty rose', 'salmon',
              'coral', 'orange red', 'chocolate', 'orage', 'gold', 'ivory', 'yellow',
              'olive', 'yellow green', 'lawn green', 'chartreuse', 'lime', 'green',
              'spring green', 'aquamarine', 'turquosie', 'azure', 'aqua', 'cyan', 
              'teal', 'lavender', 'blue', 'navy', 'navy blue', 'blue violet', 'indigo',
              'dark violet', 'plum', 'magenta', 'purple', 'red-violet', 'tan', 'beige',
              'slate gray', 'dark slate gray', 'white', 'white smoke', 'light gray',
              'sliver', 'dark gray', 'gray', 'dim gray', 'black']


def change_color(f):
    f.write('## intent: change_color\n')
    #f.write('  examples: |\n')
    for (k1,v1) in dev['device_types'].items():
        if 'color' in v1:
            dev_names = v1[0]['device']
            for dev_name in dev_names:
                for color in color_list:
                    obj = '[' + dev_name + '](' + k1 + ')'
                    if flip_coin():
                        obj  = 'the ' + obj
                    obj = add_floor(add_room(obj))
                    
                    cmd = change_color_cmd_list[random.randint(0,len(change_color_cmd_list)-1)]
                    s = Template(cmd)
                    k = random.randint(0,len(change_color_verb_list)-1)
                    s = s.safe_substitute(obj=obj,
                                          verb=change_color_verb_list[k],
                                          color=make_entity(color,'color'))
                    s = add_ask(s)
                    f.write(prefix + s + "\n")
                    
                    cmd = make_color_cmd_list[random.randint(0,len(make_color_cmd_list)-1)]
                    s = Template(cmd)
                    k = random.randint(0,len(make_color_verb_list)-1)
                    s = s.safe_substitute(obj=obj,
                                          verb=make_color_verb_list[k],
                                          color=make_entity(color,'color'))
                    s = add_ask(s)
                    f.write(prefix + s + "\n")

# intent: turn_on and turn_off

turn_on_cmd_list = ['turn $obj on', 'turn on $obj', 'switch $obj on', 'switch on $obj',
           'put $obj on', 'put on $obj', 'set $obj on', 'set on $obj',
           'power $obj up', 'power up $obj', 'flick $obj on', 
           'start $obj up', 'start up $obj', 'boot $obj up', 'boot up $obj',
           'activate $obj']
turn_off_cmd_list = ['turn $obj off', 'turn off $obj', 'swith $obj off', 'switch off $obj',
            'flick $obj off', 'deactiviate $obj', 'shut $obj down', 'shut down $obj']                    

def turn_on_off_intent(f, intent, action_list):
    f.write('## intent: ' + intent + '\n')
    #f.write('  examples: |\n')
    for (k1,v1) in dev['device_types'].items():
        if 'status' in v1:
            dev_names = v1[0]['device']
            for obj in dev_names:
                obj = make_entity(obj, k1)
                if flip_coin():
                    obj  = 'the ' + obj
                obj = add_floor(add_room(obj))
                for action in action_list:
                    s = Template(action)
                    s = s.safe_substitute(obj=obj)
                    s = add_ask(s)
                    f.write(prefix + s + "\n")
                    

prefix = '-'

random.seed(a=5436436)                    
                    
with open('nlu.md','w') as f:
    #f.write("version: '2.0'\n\n")
    #f.write('nlu:\n')
    turn_on_off_intent(f, 'turn_on', turn_on_cmd_list)
    turn_on_off_intent(f, 'turn_off', turn_off_cmd_list)
    change_color(f)
