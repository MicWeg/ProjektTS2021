from statemachine import StateMachine, State, Transition
import networkx as nx
import matplotlib.pyplot as plt
import re
import rospy
from agv.srv import *


def check_machine(machine, init_state, end_state):
    # TODO czy init_state traktowac jako zupelnie poczatkowy??
    if init_state and end_state in (machine.states_map.values()):

        for i in range(len(machine.states)):
            if machine.states[i].name == init_state:
                init_state_id = str(i)
            elif machine.states[i].name == end_state:
                end_state_id = str(i)

        list_trans_id = []
        for i in range(len(machine.transitions)):
            list_trans_id.append(machine.transitions[i].identifier)

        list_paths = []
        temp_list = []
        while True:
            for trans in list_trans_id:
                if trans[2] == init_state_id:
                    temp_list.append(trans)
                    if temp_list not in list_paths:
                        list_paths.append(temp_list)
                    print(temp_list,list_paths)
            break

    else:
        print("Unknown states")
        return None


    # return trans_list


def srv_client():
    rospy.wait_for_service('state_srv')
    try:
        state_fun = rospy.ServiceProxy('state_srv', state_srv)
        state_val = state_fun()
        state = state_val.state
        return state
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)
        return 0


def draw_graph(graph, state, pos, edge_labels,title,figure):
    plt.ion()
    plt.figure(figure)
    plt.title(title) 
    nx.draw(graph,pos,edge_color='green',width=2,linewidths=1,\
    node_size=1000,node_color='pink',\
    labels={node:node for node in graph.nodes()})
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red",font_size=5)
    nx.draw_networkx(graph.subgraph(state), pos=pos, node_color='red')


def create_trans(master_transitions,master_states,form_to):
    for indices in form_to:
        from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
        for to_idx in to_idx_tuple:  # iterate over destinations from a source state
            op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

            # create transition object and add it to the master_transitions dict
            transition = Transition(master_states[from_idx], master_states[to_idx], identifier=op_identifier)
            master_transitions[op_identifier] = transition

            # add transition to source state
            master_states[from_idx].transitions.append(transition)

if __name__ == "__main__":
    pass