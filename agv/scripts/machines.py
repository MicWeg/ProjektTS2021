from statemachine import StateMachine, State, Transition
from functions import create_trans
from generator import Generator

# Storage
# define states for a master (way of passing args to class)
options = [
    {"name": "IDLE", "initial": True, "value": "idle"},  # 0
    {"name": "Ruch do ladunku", "initial": False, "value": "Ruch do ladunku"},  # 1
    {"name": "Zgloszenie problemu", "initial": False, "value": "Zgloszenie problemu"},  # 2
    {"name": "Zaladowanie ladunku", "initial": False, "value": "Zaladowanie ladunku"},  # 3
    {"name": "Ruch do magazynu", "initial": False, "value": "Ruch do magazynu"}, # 4
    {"name": "Odlozenie ladunku", "initial": False, "value": "Odlozenie ladunku"}, # 5
    {"name": "Czekanie na zwolnienie miejsca", "initial": False, "value": "Czekanie na zwolnienie miejsca"}]  # 6

# create State objects for a master
# ** -> unpack dict to args
master_states = [State(**opt) for opt in options]
# for i in range(len(master_states)):
#     master_states[i].identifier = f'{i}'

# valid transitions for a master (indices of states from-to)
form_to = [
    [0, [0, 1]],
    [1, [2, 3]],
    [2, [0]],
    [3, [4]],
    [4, [5, 6]],
    [5, [0]],
    [6, [5]]
]

# create transitions for a master (as a dict)
master_transitions = {}

create_trans(master_transitions,master_states,form_to)
supervisor = Generator.create_master(master_states, master_transitions)



# Navigation
option_nav = [
    {"name": "Czekanie na nowy ladunek", "initial": True, "value": "Czekanie na nowy ladunek"},  # 0
    {"name": "Planowanie trasy i ruch", "initial": False, "value": "Planowanie trasy i ruch"},  # 1
    {"name": "Zatrzymanie robota", "initial": False, "value": "Zatrzymanie robota"} # 2
]

# create State objects for a master
# ** -> unpack dict to args
master_states_nav = [State(**opt) for opt in option_nav]
# for i in range(len(master_states_nav)):
#     master_states_nav[i].identifier = f'{i}'

# valid transitions for a master (indices of states from-to)
# form_to_nav = [
#     [0, [0, 1]],
#     [1, [2, 3]],
#     [2, [0]],
#     [3, [4]],
#     [4, [5, 6]],
#     [5, [0]],
#     [6, [5]]
# ]
form_to_nav = [
    [0, [1]],
    [1, [0,2]],
    [2, [0,1]]
]

# create transitions for a master (as a dict)
master_transitions_nav = {}

create_trans(master_transitions_nav,master_states_nav,form_to_nav)
navigation = Generator.create_master(master_states_nav, master_transitions_nav)