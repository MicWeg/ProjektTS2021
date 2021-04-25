from statemachine import StateMachine, State, Transition
import networkx as nx
import matplotlib.pyplot as plt
import re
from graphs import G, G_nav
import rospy
from agv.srv import *

def check_machine(machine, init_state, end_state):
    
    if init_state and end_state in (machine.states_map.values()):

        if list(machine.states_map.values())[0] == 'Czekanie na nowy ladunek':
            # TODO check if Multi is still necessary
            Gnav = nx.DiGraph(G_nav)
            paths = sorted(nx.all_simple_edge_paths(Gnav,init_state,end_state))
            trans = []
            for path in paths:
                trans_temp = []
                for connections in path:
                    for stat in machine.transitions:
                        if stat.source.name == connections[0] and stat.destinations[0].name == connections[1]:
                            trans_temp.append(stat.identifier)
                            break
                trans.append(trans_temp)

        elif list(machine.states_map.values())[0] == 'IDLE':
            paths = sorted(nx.all_simple_edge_paths(G,init_state,end_state))
            trans = []
            for path in paths:
                trans_temp = []
                for connections in path:
                    for stat in machine.transitions:
                        if stat.source.name == connections[0] and stat.destinations[0].name == connections[1]:
                            trans_temp.append(stat.identifier)
                            break
                trans.append(trans_temp)

        if not paths:
            return None
        else:
            return (paths,trans)

    else:
        print("Unknown states")
        return None



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
    plt.pause(0.1)
    # TODO try adding axis
    if title == 'Navigation':
        nx.draw(graph,pos,edge_color='green',connectionstyle='arc3,rad=0.1',width=3,linewidths=3,\
        node_size=1000,node_color='pink',\
        labels={node:node for node in graph.nodes()})
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels[0],label_pos=0.15, font_color="red",font_size=5)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels[1],label_pos=0.15, font_color="blue",font_size=5)
        nx.draw_networkx(graph.subgraph(state), pos=pos, node_color='red')
    else:
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