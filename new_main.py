from statemachine import StateMachine, State, Transition
from generator import Generator
from functions import *
import matplotlib.pyplot as plt
import networkx as nx
import re


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

# TODO Stworzyc dane do rysowania grafow - dodac pozostale grafy
G = nx.DiGraph()
G.add_edges_from([("IDLE", "Ruch do ladunku"),
                 ("Ruch do ladunku", "Zgloszenie problemu"),
                 ("Ruch do ladunku", "Zaladowanie ladunku"),
                 ("Zgloszenie problemu", "IDLE"),
                 ("Zaladowanie ladunku", "Ruch do magazynu"),
                 ("Ruch do magazynu", "Odlozenie ladunku"),
                 ("Ruch do magazynu", "Czekanie na zwolnienie miejsca"),
                 ("Odlozenie ladunku", "IDLE"),
                 ("Czekanie na zwolnienie miejsca", "Odlozenie ladunku")])
                 
edge_labels = {("IDLE", "Ruch do ladunku"): "Nowy ladunek",
               ("Ruch do ladunku", "Zgloszenie problemu"): "Nie wykryto ladunku",
               ("Ruch do ladunku", "Zaladowanie ladunku"): "Wykrycie ladunku",
               ("Zgloszenie problemu", "IDLE"): "Anulowanie zadania",
               ("Zaladowanie ladunku", "Ruch do magazynu"): "Otrzymanie punktu skladowania",
               ("Ruch do magazynu", "Odlozenie ladunku"): "Wykrycie wolnego miejsca",
               ("Ruch do magazynu", "Czekanie na zwolnienie miejsca"): "Brak wolnego miejsca",
               ("Odlozenie ladunku", "IDLE"): "Potwierdzenie wykonania zadania",
               ("Czekanie na zwolnienie miejsca", "Odlozenie ladunku"): "Wykrycie wolnego miejsca"}
               
pos = nx.spring_layout(G)


# create transitions for a master (as a dict)
master_transitions = {}
create_trans(master_transitions,master_states,form_to)


supervisor = Generator.create_master(master_states, master_transitions)
print('\n' + str(supervisor))

check_machine(supervisor, 'A', 'F')

print(f"Current state: {supervisor.current_state}\n\nPossible transitions:")
for i in form_to[0][1]:
    print(master_transitions[f'm_0_{i}'])
print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'q' to quit")

# state_name = str(supervisor.current_state)
# state_name = re.search('(?<=\')\w+', state_name).group(0)

draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie")

while True:
    try:
        inp = input()

        if inp == 'q':
            break

        master_transitions[inp]._run(supervisor)
        print(f"Current state: {supervisor.current_state}\n\nPossible transitions:")

        for i in form_to[int(inp[4])][1]:
            print(master_transitions[f'm_{int(inp[4])}_{i}'])

        print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'q' to quit")
        # state_name = str(supervisor.current_state)
        # state_name = re.search('(?<=\')\w+',state_name).group(0)
        draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie")

    except:
        print("Something went wrong. Write identifier for possible transition shown before.")






# path_1 = ["m_0_1", "m_1_2", "m_2_1", "m_1_3", "m_3_4"]
# path_2 = ["m_0_2", "m_2_3", "m_3_2", "m_2_4"]
# path_3 = ["m_0_3", "m_3_1", "m_1_2", "m_2_4"]
# paths = [path_1, path_2, path_3]

# run supervisor for exemplary path
# print("Executing path: {}".format(path))
# for event in path:

#     # launch a transition in our supervisor
#     master_transitions[event]._run(supervisor)
#     print(supervisor.current_state)

#     # add slave
#     if supervisor.current_state.value == "a":
#         # TODO: automata 1 (for) slave1
#         ...

#     if supervisor.current_state.value == "b":
#         # TODO: automata 2 (for) slave2
#         ...

#     if supervisor.current_state.value == "c":
#         # TODO: automata 3 (for) slave3
#         ...

#     if supervisor.current_state.value == "f":
#         # TODO: automata 3 (for) slave3
#         ...
#         print("Supervisor done!")

