import collections
import copy
import json
import random

# Version 2:  Move from discrete "car slot" system to float point "distance from edge"
# Assumptions:  car will always move max speed (for the edge) if it can

class TrafficManager():
    def __init__(self, network_config, car_config, tick_length=1, duration=1000):  
        self.nm = network_manager
        self.timestamp = 0
        self.tick_length = tick_length  # default: 1 second  TODO: add conversions for other ticks later
        self.sim_duration = duration    # number of ticks to run simulation for
        self.time_elapsed = 0           # +=1 per tick
        self.net = network_config
        self.car_serv = car_server    # this is the access point to the generated cars
        self.fail_to_add = []         # list of cars that could not be added
        self.inactive_cars = []       # cars who have completed their trips

    def load_new_cars_into_edge_queue(self, car_config):
        '''load new cars from JSON config.
        add new cars to their respective edge loading queues'''
        # TODO:  fix:  currently uploading straight from json for testing
        # HOW TO ACCESS ZVEZDELIN"S CAR SERVER? ==> and how to prevent multiple reads of the same file at different time stamps?
        for car_entry in car_config["car_list"]:
            new_car = Car(car_entry)
            start_edge = self.nm.edge_id_to_edge_mapping[car_entry.start_pos[0]]

            if not start_edge:
                self.fail_to_add.append(new_car)
                # raise Exception("that node does not exist")
            else:
                start_edge.waiting_cars.append(new_car)   # this is directly accessing other clas ==> fix later

    def tick(self):
        # import new cars
        self.load_new_cars_into_edge_queue()   # how to make sure same cars aren't imported again and again?  probably check some kind of dict
        edge_list = list(self.nm.edge_id_to_edge_mapping.keys()) 
        
        random.shuffle(edge_list)
        for edge in edge_list:
        # for each edge: first place any new cars
            cars_added_this_tick = []
            for new_car in edge_list.waiting_cars:
                if edge_list.place_car(new_car) == True:
                    cars_added_this_tick.append(new_car)  # add to inbound list
            # then move any existing cars forward
            for existing_car in 




class NetworkManager():
    def __init__(self, network_config):
        self.node_id_to_node_mapping = collections.defaultdict(lambda: None)
        self.edge_id_to_edge_mapping = collections.defaultdict(lambda: None)

        for node_entry in network_config["node_list"]:
            new_node = Node(node_entry)
            self.node_id_to_node_mapping[new_node.id] = new_node
            # self.node_id_to_neighbours_mapping[new_node.id] = new_node  # prepopulate nodes
        # print(self.node_id_to_node_mapping)

        for edge_entry in network_config["edge_list"]:
            new_edge = Edge(edge_entry)
            self.edge_id_to_edge_mapping[new_edge.id] = new_edge
            # the following steps directly call on Node clas ==> FIX LATER
            from_node = self.node_id_to_node_mapping[new_edge.start_node]
            from_node.outbound_edge_id_to_edge_mapping[new_edge.id] = new_edge  # node: outbound edge 
            to_node = self.node_id_to_node_mapping[new_edge.end_node]
            to_node.inbound_edge_id_to_edge_mapping[new_edge.id] = new_edge    # node: inbound edge


class Node():       # nodes only fascilitate switching edges
    def __init__(self, config) -> None:
        self.id = config["node_ID"]
        self.inbound_edge_id_to_edge_mapping = collections.defaultdict(lambda: None)
        self.outbound_edge_id_to_edge_mapping = collections.defaultdict(lambda: None) 


class Edge():
    def __init__(self, network_config):
        self.id = network_config["edge_ID"]
        self.start_node = network_config["start_node"]
        self.end_node = network_config["end_node"]
        self.length = network_config["edge_length"]    # currently in meters
        self.max_speed = network_config["max_speed"]   # currently in m/s
        
        self.max_capacity = network_config["max_capacity"]
        self.cars_on_edge = {}   # dict of cars
        self.car_on_edge_start_pos_sorted = sorted(cars_on_edge.values[1]())  # ordered list of car starts, max to min?
        self.sorted_cars_on_edge = self.sort_cars_on_edge_dict()   # function to recaulculate whenever called

        self.waiting_cars = []   # list tuple cars that are waiting to enter ==> ordered by wait time
    
    
    def sort_cars_on_edge_dict(self):
        '''create sorted dict to help with car addition checks and car movement checks'''
        sorted_dict = {}
        for pos in car_on_edge_start_pos_sorted:
            for dict_pos in cars_on_edge.values[1]():   # this assumes positions are unique ==> may cause problems later
                if cars_on_edge[dict_pos] == pos:
                    sorted_dict[dict_pos] = cars_on_edge[dict_pos]
        return sorted_dict


    def check_if_spot_available(self, car_to_add):
        '''car taken from loading queue, therefore already assumed to be on the correct edge'''
        start_pos_meter = car_to_add.start_pos[1]
        if not car_to_add.start_pos[2]:
            get_end_coord(car_to_add)
        end_pos_meter = car_to_add.start_pos[2]
        for car_front_pos in self.car_on_edge_start_pos_sorted:
            if car_front_pos < end_pos_meter:
                break  # car end has no conflict with car fronts behind its entry point
            # car_end_pos = sorted_cars_on_edge[2]    TO+DO:  fix whole if statement to index instead of value
            elif car_end_pos < start_pos_meter:
                return False  # results in overlap
                # need function to get end pos from sorted start dict ==> currently using the sorted dict
        return True

    def place_car(self, car_to_add):
        if check_if_spot_available(self, car_to_add) == True:
            return True
        else:
            return False



    # def spawn_cars(self, car):
    # '''check if cars can be added to this edge.  if so, add them.
    # cars are added before cars move because moving cars will fill in behind occupied slots'''
    # # NOTE:  need flag on cars if already processed per turn
    #     if len(self.car_order) < self.max_capacity:
    #         pass  # try to place



class Car():
    def __init__(self, config):
        self.id = config["car_id"]
        self.car_length = config["car_length"]
        self.start_pos = tuple(config["start_pos"])
        self.end_pos = tuple(config["end_pos"])
        
        self.upcoming_path = config["path"]   # replace with path calculation later
        self.edge_stack = copy.deepcopy(self.upcoming_path)
        self.edge_stack.reverse()   # reverse order for pop / next_edge function
        self.path_driven = []
        self.current_location = tuple(0, 0, 0)  # will store edge, start pos, end post

    def get_next_edge_id(self):  # derive from path computation later
        if self.edge_stack == []:
            # We are at the end of our journey!
            return None
        next_edge = self.edge_stack.pop()
        self.path_driven.append(next_edge)    # don't actually do this til confirmed
        return next_edge

    def get_terminal_point(self):
        '''returns tuple of edgeID and meter'''
        return self.end_pos

    def get_end_coord(self):
        end_loc = self.current_location[1] - self.car_length
        if end_loc < 0:
            end_loc = 0
        else:
            self.current_location[2] = end_loc




if __name__ == "__main__":
    fh_network = open('network_config.json')
    imported_network = json.load(fh_network)
    fh_network.close()

    fh_car = open('car_config.json')
    imported_cars = json.load(fh_car)
    fh_car.close()

    nm = NetworkManager(imported_network)
    tm = TrafficManager(nm, imported_cars, 1, 10)  

    while tm.time_elapsed < tm.sim_duration:
        tm.tick()
