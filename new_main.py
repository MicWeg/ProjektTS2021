from statemachine import StateMachine, State, Transition
import matplotlib.pyplot as plt
import networkx as nx
import re

# define states for a master (way of passing args to class)
options = [
    {"name": "IDLE", "initial": True, "value": "idle"},  # 0
    {"name": "A", "initial": False, "value": "a"},  # 1
    {"name": "B", "initial": False, "value": "b"},  # 2
    {"name": "C", "initial": False, "value": "c"},  # 3
    {"name": "F", "initial": False, "value": "f"}]  # 4

# create State objects for a master
# ** -> unpack dict to args
master_states = [State(**opt) for opt in options]

# valid transitions for a master (indices of states from-to)
form_to = [
    [0, [1, 2, 3]],
    [1, [2, 3, 4]],
    [2, [1, 3, 4]],
    [3, [1, 2, 4]],
    [4, []],
]

# create transitions for a master (as a dict)
master_transitions = {}
for indices in form_to:
    from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
    for to_idx in to_idx_tuple:  # iterate over destinations from a source state
        op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

        # create transition object and add it to the master_transitions dict
        transition = Transition(master_states[from_idx], master_states[to_idx], identifier=op_identifier)
        master_transitions[op_identifier] = transition

        # add transition to source state
        master_states[from_idx].transitions.append(transition)


# create a generator class
class Generator(StateMachine):
    states = []
    transitions = []
    states_map = {}
    current_state = None

    def __init__(self, states, transitions):

        # creating each new object needs clearing its variables (otherwise they're duplicated)
        self.states = []
        self.transitions = []
        self.states_map = {}
        self.current_state = states[0]

        # create fields of states and transitions using setattr()
        # create lists of states and transitions
        # create states map - needed by StateMachine to map states and its values
        for s in states:
            setattr(self, str(s.name).lower(), s)
            self.states.append(s)
            self.states_map[s.value] = str(s.name)

        for key in transitions:
            setattr(self, str(transitions[key].identifier).lower(), transitions[key])
            self.transitions.append(transitions[key])

        # super() - allows us to use methods of StateMachine in our Generator object
        super(Generator, self).__init__()

    # define a printable introduction of a class
    def __repr__(self):
        return "{}(model={!r}, state_field={!r}, current_state={!r})".format(
            type(self).__name__, self.model, self.state_field,
            self.current_state.identifier,
        )

    # method of creating objects in a flexible way (we can define multiple functions
    # which will create objects in different ways)
    @classmethod
    def create_master(cls, states, transitions) -> 'Generator':
        return cls(states, transitions)



supervisor = Generator.create_master(master_states, master_transitions)
print('\n' + str(supervisor))

# TODO Zrobic funkcje do rysowania
plt.title('Test')
G = nx.DiGraph()
G.add_edges_from([("IDLE", "A"),("A","B")])
pos = nx.spring_layout(G)   
nx.draw(G,pos,edge_color='black',width=1,linewidths=1,\
node_size=500,node_color='pink',\
labels={node:node for node in G.nodes()})
nx.draw_networkx_edge_labels(G, pos, edge_labels={("IDLE", "A"): "temp1", ("A","B"): "temp2"}, font_color="red")
nx.draw_networkx(G.subgraph('IDLE'), pos=pos, node_color='red')
plt.show()

print(f"Current state: {supervisor.current_state}")
for i in form_to[0][1]:
    print(master_transitions[f'm_0_{i}'])

print("Write 'q' to quit")

while True:
    try:
        inp = input()

        if inp == 'q':
            break

        master_transitions[inp]._run(supervisor)
        print(f"Current state: {supervisor.current_state}")

        state_name = str(supervisor.current_state)
        state_name = re.search('(?<=\')\w+',state_name)
        plt.title('Test')  
        nx.draw(G,pos,edge_color='black',width=1,linewidths=1,\
        node_size=500,node_color='pink',\
        labels={node:node for node in G.nodes()})
        nx.draw_networkx_edge_labels(G, pos, edge_labels={("IDLE", "A"): "temp1", ("A","B"): "temp2"}, font_color="red")
        nx.draw_networkx(G.subgraph(state_name.group(0)), pos=pos, node_color='red')
        plt.show()

        for i in form_to[int(inp[4])][1]:
            print(master_transitions[f'm_{int(inp[4])}_{i}'])

    except:
        print("Something went wrong. Try again")


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