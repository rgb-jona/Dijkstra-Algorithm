""" This is a module demonstrating the dijkstra algorithm by generating a grid of random nodes, connected with edges
with random weights.

Start the calculation with: dijkstra.Solver(NUM). NUM represents the number of nodes which will be
created in the net.The program limits the number to a minimum of five and a maximum of 20. If the given number is out
of this bound, the program takes a random number between 5 and 20.
There is no return value from the solver.

There is a visualisation of the grid implemented with networkx. The nodes and solutions will be printed
into the console
"""

# imports to make life easier
import random
import platform
import sys
import matplotlib.pyplot as plt

class Solver:
    """Class using the dijkstra algorithm on a dataset created by the Randomizer-class"""
    def __init__(self, number_of_nodes=0):
        # try importing networkx for pretty plot at end of programm
        try:
            import networkx
            # check if python platform version is 3.8.XX and above
            if int(platform.python_version()[2]) >= 8:
                print("*" * 60 + "\nGraphics could not be supported due to problems between Python greater 3.8.XX"
                               "and networkx.\n Please consider using a Python Version below 3.8.XX if graphics cant be shown\n" + "*" * 60)
                self.__use_graphics = False
            # set the option for using networkx as True to support graphical plotting of the network
            self.__use_graphics = True
        except ModuleNotFoundError:
            print("*" * 60 + "\nTo show the nodes in a plot please install networkx:\n$"
                              "pip install networkx[all]\n" + "*" * 60)
            self.__use_graphics = False

        # initialize variables
        self.__randomizer = Randomizer(number_of_nodes)
        self.__node_array = self.__randomizer.create_node_array()
        # create dictionary with all nodes to make access easier
        self.__node_dic = {}
        for element in self.__node_array:
            self.__node_dic[element.get_name()] = element

        # choose a random start node out of node array and pop it out of the array
        self.__start_node = self.__node_array.pop(random.randint(0, len(self.__node_array)-1))
        # call solve with the chosen start node
        self.solve(self.__start_node)

        # debug print
        print("Start node: " + self.__start_node.get_name())
        print()
        for element in self.__node_dic:
            print(self.__node_dic.get(element))
        if self.__use_graphics:
            self.__plot_network()

    def solve(self, node):
        # take connections of the nodes and compare the connected values
        for element in node.get_connections():
            # get node which is connection to out of dictionary
            node_connected_to = self.__node_dic.get(element)
            # check if the node has already been visited
            if not node_connected_to.get_visited():
                # get the value of the node_connected_to
                node_connected_to_value = node_connected_to.get_value()
                # calculate new node value based on the connection weight and value of the actual node
                node_connected_to_new_value = node.get_value() + \
                                              node.get_connections().get(node_connected_to.get_name())
                # if the node_connected_to's value is 0 or bigger, than the value of node plus the connection weight,
                # the new value of node_connected_to is: value of node plus the connection weight
                if node_connected_to_value == 0 or node_connected_to_value > node_connected_to_new_value:
                    node_connected_to.set_value(node_connected_to_new_value)
                    # set node as the previous node of
                    node_connected_to.set_previous_node(node.get_name())
                    # overwrite the node_connected_to in the dic
                    self.__node_dic[node_connected_to.get_name()] = node_connected_to

        # mark node as visited
        node.set_visited()
        # exit condition for the recursive function
        if len(self.__node_array) == 0:
            return 0

        # make temp array to store the nodes with the lowest value which is not zero
        temp_node_array = []
        for element in self.__node_array:
            if element.get_value() != 0:
                temp_node_array.append(element)

        # get node with lowest value out of the array
        position = 0
        min_value = temp_node_array[position].get_value()
        for iterator in range(1, len(temp_node_array)):
            current_node_value = temp_node_array[iterator].get_value()
            if min_value > current_node_value:
                min_value = current_node_value
                position = iterator
        node_with_smallest_value = temp_node_array[position]

        # remove temp_node_array to save memory
        del temp_node_array
        # perform solve on the node with the smallest value not equalling 0 out of self.__node_array
        # also popping it out of self.__node_array to get a exit condition for the recursive function
        self.solve(self.__node_array.pop(self.__node_array.index(node_with_smallest_value)))

    def __plot_network(self):
        """function to plot the given data into a figure to help orienting"""
        # this should be made better later:
        import networkx as nx
        # check if networkx is imported
        if "networkx" not in sys.modules:
            raise ModuleNotFoundError

        # create graph
        plot = nx.Graph()
        # add node for each node in self.__node_dic
        for element in self.__node_dic:
            current_node = self.__node_dic.get(element)
            current_node_name = current_node.get_name()
            plot.add_node(current_node_name, label=current_node_name, node_size=500)

        # add edges between all the nodes
        for element in self.__node_dic:
            # get current node out of self.__node_dic
            current_node = self.__node_dic.get(element)
            # extract connections
            current_node_connections = current_node.get_connections()
            # draw connections
            for element in current_node_connections:
                plot.add_edge(current_node.get_name(), element
                              , label=current_node.get_connections().get(element))

        # create color map to give start point a different look
        color_map = len(self.__node_dic)*['green']
        color_map[ord(self.__start_node.get_name())-97] = 'red'
        # get edge labels
        labels = nx.get_edge_attributes(plot, 'label')
        # position nodes circular
        pos = nx.circular_layout(plot)
        # plot node diagram
        nx.draw(plot, pos, node_color=color_map, with_labels=True)
        nx.draw_networkx_edge_labels(plot, pos, edge_labels=labels)
        plt.draw()
        plt.show()


class Randomizer:
    """simple class to manage the creation of a pattern of nodes in which my
                                    implementation of the dijkstra algorithm can work"""
    def __init__(self, number_of_nodes=0):
        # pre initialize all variables in class to have better overview over them
        self.__number_of_nodes = 0

        # initialize random module
        random.seed()

        # if the chosen number of nodes is to small or not given, a random number is made up and stored
        # in self.__number_of_nodes
        if number_of_nodes < 5 or number_of_nodes > 20:
            self.__number_of_nodes = random.randint(5,20)
        else:
            self.__number_of_nodes = number_of_nodes


    def create_node_array(self):
        """This function creates a random grid made out of objects from type node with weighted connections to other
        nodes and returns it as array"""
        # get information how many nodes should be in the grid
        number_of_nodes = self.__number_of_nodes
        node_array = []
        # prefix for name
        # add a number_of_nodes random nodes to the node_array
        while number_of_nodes != 0:
            # make new instance of node with a generated name
            node_name = chr(97 + (self.__number_of_nodes - number_of_nodes))
            node_array.append(Node(node_name))
            number_of_nodes -= 1

        # iterate through nodes and make connections
        all_connected = False
        # iterate till there are at least two connections for every node
        while not all_connected:
            # pick one node and randomly make connection
            for iterator in range(0, len(node_array)):
                if random.randint(0, 1):
                    actual_node = node_array[iterator]
                    node_array = actual_node.create_connection(node_array)

            # check if all nodes have at least 2 connections
            for element in node_array:
                if element.get_number_of_connections() < 2:
                    break
                # if all nodes have two connections and element is the last element of the node_array exit the loop
                elif node_array.index(element) == len(node_array)-1:
                    all_connected = True
        return node_array



class Node:
    def __init__(self, node_name):
        # add needed arguments to object and pre initialize all others
        self.__name = node_name
        # pre initialize dic to store connections between this node and the other nodes into
        self.__connections = {}
        # normally the initial value of the node is "inf" but python does not support this and the value of a node never
        # will be 0
        self.__value = 0
        self.__previous_node = " "
        # variable to mark node as visited
        self.__visited = False

    def create_connection(self, node_array):
        # set a max number of connections
        max_connections = len(node_array)
        # make sure that there is not more than one connection to each other node
        if len(self.__connections) < max_connections:
            # randomly choose node to connect to
            node_number_to_connect_to = random.randint(0, len(node_array)-1)
            node_to_connect_to = node_array[node_number_to_connect_to]
            # check if the node_to_connect_to has already max_connection connections, if the node_to_connect is
            # self (and self want to make a connection with itself) and if there is already a connection from self
            # to node_to_connect
            if node_to_connect_to.get_number_of_connections() < max_connections and self != node_to_connect_to\
                    and (node_to_connect_to.get_name() not in self.__connections):
                # get a random weight for the connection
                connection_weight = random.randint(1, 100)
                # save the information about this connection in self and the node_to_connect in addition overwrite the
                # corresponding nodes (to self and node_to_connect) in the node_array
                node_array[node_array.index(self)] = self.add_connection(node_to_connect_to, connection_weight)
                node_array[node_number_to_connect_to] =\
                    node_to_connect_to.add_connection(self, connection_weight)
        return node_array


    def add_connection(self, node, weight):
        # add the connection to node and the weight in the __connections dic of self
        self.__connections[node.get_name()] = weight
        return self


    # getter and setter functions
    def get_visited(self):
        return self.__visited

    def set_visited(self):
        self.__visited = True
        return 0

    def get_number_of_connections(self):
        return len(self.__connections)

    def get_name(self):
        return self.__name

    def get_connections(self):
        return self.__connections

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
        return 0

    def set_previous_node(self, node_name):
        self.__previous_node = node_name
        return 0

    def get_previous_node(self):
        return self.__previous_node


    # overloaded functions
    def __str__(self):
        return "Node: " + self.get_name() + "   Value: " + str(self.get_value()) + "   Previous Node: " + self.get_previous_node()\
               + "   Conn: " + str(len(self.__connections)) + "   Connections: " + str(self.__connections)

    def __ne__(self, other):
        if type(self) == type(other):
            if self.__name == other.get_name():
                return False
        return True