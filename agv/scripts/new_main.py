#!/usr/bin/env python
from statemachine import StateMachine, State, Transition
from functions import *
# import re
# import matplotlib.pyplot as plt
from machines import *
from graphs import *
import time


print('\n' + str(supervisor))

# check_machine(supervisor, 'Ruch do ladunku', 'IDLE')


print(f"Current state: {supervisor.current_state}\n\nPossible transitions:")
for i in form_to[0][1]:
    print(master_transitions[f'm_0_{i}'])
print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'q' to quit")

# state_name = str(supervisor.current_state)
# state_name = re.search('(?<=\')\w+', state_name).group(0)

draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie",1)

while True:
    try:
        inp = input()

        if inp == 'q':
            break

        master_transitions[inp]._run(supervisor)
        print(f"Current state: {supervisor.current_state}\n\nPossible transitions:")

        for i in form_to[int(inp[4])][1]:
            print(master_transitions[f'm_{int(inp[4])}_{i}'])
            

        if supervisor.current_state.name == "Ruch do ladunku":
            print("\nWaiting for state response from robot")
            flag = 0
            state_flag = 10
            while flag == 0:
                state = srv_client()

                if state == 0 and state != state_flag:
                    draw_graph(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav, "Navigation", 2)
                    state_flag = state
                elif state == 1 and state != state_flag:
                    master_transitions_nav['m_0_1']._run(navigation)
                    draw_graph(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav, "Navigation", 2)
                    state_flag = state
                    
                    # if state == 1:
                    #     master_transitions_nav['m_0_1']._run(navigation)
                    #     while state == 1:
                    #         state = srv_client(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav)
            

        print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'q' to quit")
        # state_name = str(supervisor.current_state)
        # state_name = re.search('(?<=\')\w+',state_name).group(0)
        draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie",1)

    except Exception as e:
        print(e)







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

