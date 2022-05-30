import collections
import copy
import json
import random

# Version 2:  Move from discrete "car slot" system to float point "distance from edge"
# Assumptions:  car will always move max speed (for the edge) if it can

class TrafficManager():
    def __init__(self, network_config, car_config, tick_length=1):  
        self.nm = network_manager
        self.timestamp = 0
        self.tick_length = tick_length  # default: 1 second  TODO: add conversions for other ticks later
        self.net = network_config
        self.car_serv = car_server    # this is the access point to the generated cars
        self.fail_to_add = []         # list of cars that could not be added

    def load_new_cars_into_edge_queue(self, car_config):
        '''load new cars from JSON config.
        add new cars to their respective edge loading queues'''
        for car_entry in car_config["car_list"]:
            new_car = Car(car_entry)
            start_edge = self.nm.edge_id_to_edge_mapping[car_entry.start_pos[0]]

            if not start_edge:
                self.fail_to_add.append(new_car)
                # raise Exception("that node does not exist")
            else:
                start_edge.waiting_cars.append(new_car)   # this is directly accessing other clas ==> fix later

    def tick(self):
        # for each edge: first place any new cars
        # then move any existing cars forward
        # TODO: shuffle starting edge each time to balance


class Edge():
    def __init__(self, network_config):
        self.id = network_config["edge_ID"]
        self.start_node = network_config["start_node"]
        self.end_node = network_config["end_node"]
        self.length = network_config["edge_length"]    # currently in meters
        self.max_speed = network_config["max_speed"]   # currently in m/s
        
        self.max_capacity = network_config["max_capacity"]
        self.cars_on_edge = {}   # dict of cars
        self.car_on_edge_start_positions_sorted = sorted(cars_on_edge.values[1]())  # ordered list of car starts, max to min?
        
        self.waiting_cars = []   # list tuple cars that are waiting to enter ==> ordered by wait time
    
    # need function to get end pos from sorted start dict

    def check_if_spot_available(self, car_to_add):
        '''car taken from loading queue, therefore already assumed to be on the correct edge'''
        start_pos_meter = car_to_add.start_pos[1]
        if not car_to_add.start_pos[2]:
            get_end_coord(car_to_add)
        end_pos_meter = car_to_add.start_pos[2]
        for car_front_pos in self.car_on_edge_start_positions_sorted:
            if car_front_pos < end_pos_meter:
                break  # car end has no conflict with car fronts behind its entry point
            elif 



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