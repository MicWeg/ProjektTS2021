from statemachine import StateMachine, State, Transition
import networkx as nx
import matplotlib.pyplot as plt
import re
from graphs import G, G_nav
# import rospy
# from agv.srv import *

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

    #     for i in range(len(machine.states)):
    #         if machine.states[i].name == init_state:
    #             init_state_id = str(i)
    #         elif machine.states[i].name == end_state:
    #             end_state_id = str(i)

        # list_trans_id = []
        # for i in range(len(machine.transitions)):
        #     list_trans_id.append(machine.transitions[i].identifier)

    #     list_paths = []
    #     for trans in list_trans_id:
    #         if trans[2] == init_state_id:
    #             temp_list = []
    #             temp_list.append(trans)
    #             if temp_list not in list_paths:
    #                 list_paths.append([temp_list])
    #             for i in range(len(list_trans_id)):
    #                 temp_trans = list_trans_id.copy()
    #                 for trans_new in temp_trans:
    #                     if trans_new[2] == temp_list[-1][4] and trans_new not in temp_list:
    #                         temp_list.append(trans_new)
    #                         temp_trans.remove(trans_new)
    #                     if [temp_list] not in list_paths:
    #                         list_paths.append([temp_list])


    #     flag_start = 0
    #     flag_end = 0
    #     trans_list = []

    #     for paths in list_paths:
    #         for i in range(len(paths[0])):
    #             if paths[0][i][2] == init_state_id:
    #                 flag_start = 1
    #                 start_id = i
    #             if paths[0][i][4] == end_state_id:
    #                 flag_end = 1
    #                 end_id = i
    #         if flag_start == 1 and flag_end == 1 and start_id <= end_id and paths[0][start_id:end_id+1] not in trans_list:
    #             trans_list.append(paths[0][start_id:end_id+1])
    #         flag_end = 0
    #         flag_start = 0

    #     if not trans_list:
    #         return None
    #     else:
    #         return trans_list
        if not paths:
            return None
        else:
            return (paths,trans)

    else:
        print("Unknown states")
        return None



# def srv_client():
#     rospy.wait_for_service('state_srv')
#     try:
#         state_fun = rospy.ServiceProxy('state_srv', state_srv)
#         state_val = state_fun()
#         state = state_val.state
#         return state
#     except rospy.ServiceException as e:
#         print("Service call failed: %s" % e)
#         return 0


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