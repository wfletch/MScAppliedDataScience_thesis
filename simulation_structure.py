import random
import math
import json
import numpy as np


####### defaults #######
default_network = 'network0.json'
default_cars = 'cars0.json'


####### generate synthetic input data  #######
class synthetic_data():
    def is_neighbour(start_node_index, list_of_nodes, threshold_value):
        ''' remove the start_node from the list_of_nodes.
        for each remaining node, generate a number.
        if the number is less than threshold_value, append to neighbours_list
        '''
        other_nodes = list_of_nodes
        del other_nodes[start_node_index]

        neighbours_list = []
        for node in other_nodes:
            compare_value = random.random()
            if compare_value < threshold_value:
                neighbours_list.append(node)

        return neighbours_list


    def generate_network(number_nodes, hubs_yesno = no, connection_probability, output_network_filename):
        ''' specify a number of nodes for the synthetic network and the probability (0<p<=1) that any two nodes will be connected. 
        this random graph will be output to a json file called output_filename, and contains a list of nodes and a list of neighbours per node.
        default is no nodes are hubs.
        NOTE!  All paths will be assumed as one-way!  Therefore A==>B does not imply that B==>A exists!
        '''
        # TODO:  add logic where start and end hubs may be the same

        generated_node_list = []
        for node_ID in range(number_nodes):
            generated_node_list.append(node_ID)

        neighbours_dict = {start_node : is_neighbour(start_node, generated_node_list, connection_probability) for start_node in generated_node_list}

        start_network_hubs = [] 
        start_hub_prob_list = []
        start_nodes_prob_list = []
        end_network_hubs = []
        end_hub_prob_list = []
        end_nodes_prob_list = []

        if hubs_yesno == yes:
            max_hubs = ceil((number_nodes + 1)/2)  # no more than half the nodes can be hubs, TODO: set global threshold percent later
            min_hubs = 1                      # TODO: set as global variable later
            start_hub_count = random.randint(min_hubs, max_hubs)
            end_hub_count = random.randint(min_hubs, max_hubs)
            min_probability = 1/number_nodes
            for i in start_hub_count:
                start_network_hubs.append(random.choice(generated_node_list))
                start_hub_prob_list.append(random.choice(range(min_probability, number_nodes*min_probability)))   # TODO:  check that final prob sum of hubs never exceeds 1 -- should already be true
                end_network_hubs.append(random.choice(generated_node_list))
                end_hub_prob_list.append(random.choice(range(min_probability, number_nodes*min_probability)))

        start_nodes_prob_list = node_weights(generated_node_list, start_network_hubs, start_hub_prob_list)
        end_nodes_prob_list = node_weights(generated_node_list, end_network_hubs, end_hub_prob_list)

        # TODO: write json with: nodes, neighbours, generate IDs for edges, hubs list (start/end), prob per node (start/end)


    def node_weights(node_list, hub_list = [], hub_weight_list = []):
        ''' hubs are nodes that are more likely to be start or end positions (ex: major cities).  The default is no hubs.
        input a list of hubs.  input a list of portion of traffic each hub is responsible for.  all other nodes are assumed to be equally likely.
        ex: hub_list = [a,b] , hub_weight_list [0.5,0.4]
        outputs a list of node probabilities
        '''
        num_nodes = len(node_list)
        num_hubs = len(hub_list)
        total_hub_weight = sum(hub_weight_list)

        nonhub_prob = (1 - total_hub_weight) / (num_nodes - num_hubs)

        prob_list = num_nodes * [nonhub_prob]  # unadjusted
        for prob in prob_list:  # correct values 
            corresponding_node = node_list[prob]
            if corresponding_node in hub_list:
                hub_index = hub_list.index(corresponding_node)
                prob = hub_weight_list[hub_index]
        
        return prob_list
        # TODO: there must be a smarter way to do this rather than tripling/quadruplings/etc the list size.  come back later


    def generate_cars(number_cars, node_list, start_hub_prob_list, end_hub_prob_list, output_car_filename):
        ''' specify a number of car objects to create.  
        the cars will be randomly populated with data derived from network attributes and default decision functions
        '''
        generated_cars = []

        for car_ID in range(number_cars):
            start_node = np.random.choice(node_list, start_hub_prob_list)
            end_node = np.random.choice(node_list, end_hub_prob_list)
            decision_logic = 
            new_car = car(car_ID, start_node, end_node, decision_logic, [], [])

        pass
        # TODO: write json


####### simulation classes #######
class network():
    node_list = []
    edge_list = []
    car_list = []

    start_network_hubs = []   # depending on commutes/time of day of simulation, start and end hubs may be different or have different probabilities -- ONLY NEED FOR ADDING/REMOVING codes/edges/cars
    start_hub_prob_list = []
    end_network_hubs = []
    end_hub_prob_list = []

    def __init__(self, network_name, network_json = default_network, cars_json = default_cars, runtime = 60):
        ''' import underlying network and cars.
        the simulation will run for runtime ticks.
        each tick will push a new state to the server to display.
        when runtime = 0, output final state, errors, and statistics
        '''
        self.name = network_name
        self.imported_network_file = network_json
        self.imported_cars_file = cars_json

        # read network_json and append to node_list and edge_list
        # TODO separate node and edge parts of input file

        # read cars_json
        pass

    def tick(elapsed_time):
        while elapsed_time < runtime:
            # DO THE THING
            pass


class car():
    def __init__(self, car_ID, start_node, end_node, decision_logic = rand, planned_route, complete_route):
        ''' create object car and populate with attributes.
        car_ID, start_node, end_node, decision_logic are imported from the input car json file.
        planned_route, complete_route are generated by route_calc function and updated with each tick.  joining these two values gives a whole route overview.
        decision_logic is how that particular car chooses one route over another - choose from rand (for random), shortest, or cheapest (for tolls).
        '''
        pass




    




