#!/usr/bin/env python
from statemachine import StateMachine, State, Transition
from functions import *
# import re
# import matplotlib.pyplot as plt
import time
from machines import *
from graphs import *


print(f"Current state: {supervisor.current_state}\n\nPossible transitions:")
for i in form_to[0][1]:
    print(master_transitions[f'm_0_{i}'])
print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'q' to quit")

# state_name = str(supervisor.current_state)
# state_name = re.search('(?<=\')\w+', state_name).group(0)

draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie",1)

# TODO add option to use check_machine from consol
# print(check_machine(supervisor, 'Ruch do ladunku', 'Czekanie na zwolnienie miejsca'))

    
while True:
    try:
        inp = input()

        if inp == 'q':
            break

        master_transitions[inp]._run(supervisor)
        print(f"Current state: {supervisor.current_state}\n\nPossible transitions:")

        for i in form_to[int(inp[4])][1]:
            print(master_transitions[f'm_{int(inp[4])}_{i}'])
            
        # TODO add for different states needing navigation //// Maybe ignore changing here and only draw once and write states in console?
        if supervisor.current_state.name == "Ruch do ladunku":
            # draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie",1)

            while True:
                try:
                    state = srv_client()
                    if state == 0:
                        draw_graph(G_nav, "IDLE", pos_nav, edge_labels_nav, "Navigation", 2)
                    if state == 1:
                        draw_graph(G_nav, "A", pos_nav, edge_labels_nav, "Navigation", 2)

                except Exception as e:
                    print(e)
            
        
        #     while flag == 0:
        #         print("\nWaiting for state response from robot\nPress 'Enter' to check state or 'q' to leave")
        #         # bufor = 0
        #         global value
        #         print(value)
        #         srv_client()
        #         draw_graph(G_nav, "IDLE", pos_nav, edge_labels_nav, "Navigation", 2)
        #         time.sleep(5)
        #         master_transitions_nav["m_0_1"]._run(navigation)
        #         print(f"Current state: {navigation.current_state}")
        #         draw_graph(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav, "Navigation", 2) 


        #         if value[0] == 1:
        #             master_transitions_nav["m_0_1"]._run(navigation)
        #             print(f"Current state: {navigation.current_state}")
        #             draw_graph(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav, "Navigation", 2) 
        #         if value[0] == 0 and flags == 0:
        #             flags = 1
        #             print(True)
        #             # draw_graph(G_nav, "IDLE", pos_nav, edge_labels_nav, "Navigation", 1)
        #             plt.figure(2)
        #             plt.show(block=False)
        #             time.sleep(5)
        #         key = input()
        #         # state_nr = 0
        #         if key == "":
        #             state = srv_client()
        #         elif key == "q":
        #             break

        #         # TODO change ._run if already in state
        #         # TODO do we need to use ._run in this case ? or is it obsolete? - there is a possibility of missing a state
        #         if state == 0:
        #             # if state_nr != 0:
        #             #     state_nr = 0

        #             print(f"Current state: IDLE")
        #             draw_graph(G_nav, "IDLE", pos_nav, edge_labels_nav, "Navigation", 2)
        #         elif state == 1:
        #             master_transitions_nav["m_0_1"]._run(navigation)
        #             print(f"Current state: {navigation.current_state}")
        #             draw_graph(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav, "Navigation", 2)            

        print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'q' to quit")
        # state_name = str(supervisor.current_state)
        # state_name = re.search('(?<=\')\w+',state_name).group(0)
        draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie",1)

    except Exception as e:
        print(e)