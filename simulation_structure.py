import collections
import copy
import json
import random

# Version 2:  Move from discrete "car slot" system to float point "distance from edge"
# Assumptions:  car will always move max speed (for the edge) if it can

class TrafficManager():
    def __init__(self, network_config, car_server, tick_length=1):  
        self.timestamp = 0
        self.tick_length = tick_length  # default: 1 second  TODO: add conversions for other ticks later
        self.net = network_config
        self.car_serv = car_server    # this is the access point to the generated cars



class Edge():
    def __init__(self, network_config):
        self.id = network_config["edge_ID"]
        self.start_node = network_config["start_node"]
        self.end_node = network_config["end_node"]
        self.length = network_config["edge_length"]    # currently in meters
        self.max_speed = network_config["max_speed"]   # currently in m/s
        self.max_capacity = network_config["max_capacity"]
        self.car_order = []   # keeps track of cars currently on road ==> list of TUPLE car.id, car.pos
        self.waiting_cars = []   # list tuple cars that are waiting to enter ==> ordered by wait time
    
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
        self.start_node = config["start_node"]
        self.end_node = config["end_node"]
        
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
        return self.end_node

    def get_end_coord(self):
        end_loc = self.current_location[1] - self.car_length
        if end_loc < 0:
            end_loc = 0
        else:
            self.current_location[2] = end_loc