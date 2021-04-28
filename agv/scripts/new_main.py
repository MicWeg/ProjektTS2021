#!/usr/bin/env python3
from statemachine import StateMachine, State, Transition
from functions import *
from machines import *
from graphs import *
import rospy
from std_msgs.msg import Bool

rospy.init_node('agv_node')
pub = rospy.Publisher('/mir_move_next', Bool, queue_size=10)

print(f"Current state: {supervisor.current_state}\n\nPossible transitions:")
for i in form_to[0][1]:
    print(master_transitions[f'm_0_{i}'])

print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'c' to check machine. Write 'q' to quit")




draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie",1)
draw_graph(G_nav, "Czekanie na nowy ladunek", pos_nav, edge_labels_nav, "Navigation", 2)

while True:
    try:
        inp = input('Input: ')

        if inp == 'q':
            break

        if inp == 'c':
            try:
                mach = input('\nMachines: \'supervisor\', \'navigation\'.\nChoose machine: ')
                init = input('Write init state: ')
                end = input('Write end state: ')
                if mach == 'supervisor':
                    print(f'Transitions: {check_machine(supervisor, init, end)}')
                elif mach == 'navigation':
                    print(f'Transitions: {check_machine(navigation, init, end)}')
                else:
                    print('Unknown machine')

            except Exception as e:
                print(e)
                break
            print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'c' to check machine. Write 'q' to quit")

        
        if inp != 'c':
            master_transitions[inp]._run(supervisor)
            draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie",1)
            if supervisor.current_state.name == "Ruch do ladunku" or supervisor.current_state.name == "Ruch do magazynu":
                draw_graph(G, supervisor.current_state.name, pos, edge_labels,"Magazynowanie",1)
                print("Waiting for robots to finish moving\n")
                for i in range(10):
                        pub.publish(True)
                        rospy.sleep(i*0.1)
                while True:
                    try:
                        state = srv_client()
                        if state == 3:
                            if navigation.current_state.name== "Planowanie trasy i ruch":
                                master_transitions_nav["m_1_0"]._run(navigation)
                                draw_graph(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav, "Navigation", 2)
                                break
                            elif navigation.current_state.name == "Zatrzymanie robota":
                                master_transitions_nav["m_2_0"]._run(navigation)
                                draw_graph(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav, "Navigation", 2)
                                break

                        elif state == 1:
                            if navigation.current_state.name == "Czekanie na nowy ladunek":
                                master_transitions_nav["m_0_1"]._run(navigation)
                            elif navigation.current_state.name == "Zatrzymanie robota":
                                master_transitions_nav["m_2_1"]._run(navigation)

                        elif state == 2:
                            if navigation.current_state.name == "Planowanie trasy i ruch":
                                master_transitions_nav["m_1_2"]._run(navigation)

                        draw_graph(G_nav, navigation.current_state.name, pos_nav, edge_labels_nav, "Navigation", 2)

                    except Exception as e:
                        print(e)

            print(f"Current state: {supervisor.current_state}\n\nPossible transitions:")
            for i in form_to[int(inp[4])][1]:
                print(master_transitions[f'm_{int(inp[4])}_{i}'])

            print("\nTo transition from one state to another write identifier (visible above) for that transition (for example 'm_0_1'). Write 'c' to check machine. Write 'q' to quit")

    except Exception as e:
        print(f'Wrong input :{e}')
