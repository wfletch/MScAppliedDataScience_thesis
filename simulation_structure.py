import collections
import json
from tracemalloc import start

class TrafficManager():
    def __init__(self, network_manager, car_config):
        self.nm = network_manager
        self.fail_to_add = []
        # self.car_id_to_car_mapping = {}

        for car_entry in car_config["car_list"]:
            new_car = Car(car_entry)
            # self.car_id_to_car_mapping[new_car.id] = new_car
            if not self.nm.place_new_car(new_car):
                self.fail_to_add.append(new_car)

        
    def tick():
        pass


class NetworkManager():
    def __init__(self, network_config):
        self.node_id_to_node_mapping = collections.defaultdict(lambda: None)
        self.edge_id_to_edge_mapping = {}

        for node_entry in network_config["node_list"]:
            new_node = Node(node_entry)
            self.node_id_to_node_mapping[new_node.id] = new_node
        print(self.node_id_to_node_mapping)

        for edge_entry in network_config["edge_list"]:
            new_edge = Edge(edge_entry)

            self.edge_id_to_edge_mapping[new_edge.id] = new_edge

            from_node = self.node_id_to_node_mapping[new_edge.start_node]
            from_node.outbound_edge_id_to_edge_mapping[new_edge.id] = new_edge

            to_node = self.node_id_to_node_mapping[new_edge.end_node]
            to_node.inbound_edge_id_to_edge_mapping[new_edge.id] = new_edge
        print(self.edge_id_to_edge_mapping)

    def place_new_car(self, car_entry):
        # what if we don't have space?
        # what if the start node DNE?
        start_node = self.node_id_to_node_mapping[car_entry.start_node]
        if not start_node:
            return False
            # raise Exception("dude, that fucking node does not fucking exist")
        start_node.add_pre_load_car(car_entry)






class Node():
    def __init__(self, config) -> None:
        self.id = config["node_ID"]
        self.inbound_edge_id_to_edge_mapping = {}
        self.outbound_edge_id_to_edge_mapping = {}
        self.pre_loaded_cars = []

    def add_pre_load_car(self, car):   # rename accurately later
        # some logic to check if it's even possible?
        # maybe delete and replace with direct edge placement instead
        self.pre_loaded_cars.append(car)
    
    def check_outbound_opening(self, outbound_edge):
        '''see if the first position is occupied.  If not, opening possible'''
        if not outbound_edge:
            return False 
            # exception needed:  car cannot move as intended, see if recalculation possible
        elif outbound_edge.queue[0]:
            return False
        return True

    def check_inbound_car_waiting(self, inbound_edge):
        '''see if car in last position, if so return True'''
        if inbound_edge.queue[-1]:
            return True

    def get_car_ID(self, inbound_edge):
        return inbound_edge.queue.pop()

    

    def move_car(self):

    

class Edge():
    def __init__(self, config) -> None:
        self.id = config["edge_ID"]
        self.start_node = config["start_node"]
        self.end_node = config["end_node"]
        self.length = config["edge_length"]
        self.queue = collections.deque([None] * self.length, maxlen=self.length)

class Car():
    def __init__(self, config) -> None:
        self.id = config["car_ID"]
        self.start_node = config["start_node"]
        self.end_node = config["end_node"]
        self.path = config["path"]   # replace with path calculation later



if __name__ == "__main__":
    fh_network = open('network_config.json')
    imported_network = json.load(fh_network)

    fh_network.close()
    # print(imported_network)


    fh_car = open('car_config.json')
    imported_cars = json.load(fh_car)

    fh_car.close()
    # print(imported_cars)
    nm = NetworkManager(imported_network, imported_cars)
    tm = TrafficManager(nm)





# class edge():







# class car():








class traffic_manager():
    def __init__(self):
        pass

    def move():
        pass


    