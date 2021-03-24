from statemachine import StateMachine, State, Transition
import networkx as nx
import matplotlib.pyplot as plt
import re


def check_machine(machine, init_state, end_state):
    # TODO czy init_state traktowac jako zupelnie poczatkowy??
    if init_state and end_state in (machine.states_map.values()):
        # TODO przejsc do init_state i sprobowac przejsc do end_state
        # print(machine.transitions)
        pass
    else:
        print("Unknown states")
        return None


    # return trans_list


def draw_graph(graph, state, pos, edge_labels,title):
    plt.ion()
    plt.title(title) 
    nx.draw(graph,pos,edge_color='black',width=1,linewidths=1,\
    node_size=500,node_color='pink',\
    labels={node:node for node in graph.nodes()})
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red")
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