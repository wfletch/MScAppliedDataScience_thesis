import collections
import copy
import json
import random

class TrafficManager():
    def __init__(self, network_manager, car_config):
        self.nm = network_manager
        self.tick_count = 0
        self.fail_to_add = []
        # self.car_id_to_car_mapping = {}

        for car_entry in car_config["car_list"]:
            new_car = Car(car_entry)
            # self.car_id_to_car_mapping[new_car.id] = new_car
            if not self.nm.place_new_car(new_car):
                self.fail_to_add.append(new_car)


    def output_network_state(self):
        '''set up later: export json of state to use for visualizer'''
        network_dump = {}
        #network_dump["node_list"] = json.dumps(self.nm.node_id_to_node_mapping)
        #network_dump["edge_list"] = json.dumps(self.nm.edge_id_to_edge_mapping)
        network_dump["cars_misc"] = {                           # ==> either overwrite string function or do something else
            "number_failed_to_add": len(self.fail_to_add),
            "number_car_routes_completed": len(self.nm.inactive_cars)
        }
        print(network_dump)

        
    def tick(self):
        print("TICK:", self.tick_count)    
        self.nm.tick()
        self.tick_count+=1


class NetworkManager():
    def __init__(self, network_config):
        self.node_id_to_node_mapping = collections.defaultdict(lambda: None)
        self.edge_id_to_edge_mapping = collections.defaultdict(lambda: None)
        # self.node_id_to_neighbours_mapping = collections.defaultdict(lambda: None)  
        self.inactive_cars = []     # cars who have completed their trips

        for node_entry in network_config["node_list"]:
            new_node = Node(node_entry)
            self.node_id_to_node_mapping[new_node.id] = new_node
            # self.node_id_to_neighbours_mapping[new_node.id] = new_node  # prepopulate nodes
        # print(self.node_id_to_node_mapping)

        for edge_entry in network_config["edge_list"]:
            new_edge = Edge(edge_entry)

            self.edge_id_to_edge_mapping[new_edge.id] = new_edge

            from_node = self.node_id_to_node_mapping[new_edge.start_node]
            from_node.outbound_edge_id_to_edge_mapping[new_edge.id] = new_edge  # node: outbound edge

            to_node = self.node_id_to_node_mapping[new_edge.end_node]
            to_node.inbound_edge_id_to_edge_mapping[new_edge.id] = new_edge    # node: inbound edge

            # self.node_id_neighbours[from_node.id].append(to_node.id) # node: neighbour node  # FIX SYNTAX
            #  next iteration: append to dict: (to_node.id, new_edge.length)

        # print(self.edge_id_to_edge_mapping)

    def place_new_car(self, car_entry): #None
        # what if we don't have space?
        start_node = self.node_id_to_node_mapping[car_entry.start_node]
        if not start_node:
            return False
            # raise Exception("that node does not exist")
        start_node.add_pre_load_car(car_entry)
        return True

    def tick(self):     
        node_list = list(self.node_id_to_node_mapping.keys())   
        edge_list = list(self.edge_id_to_edge_mapping.keys())   
        random.shuffle(node_list)   # ensure no node nor edge's inbound traffic favoured
        for node_id in node_list:
            node = self.node_id_to_node_mapping[node_id]
            node.node_tick()
        for edge_id in edge_list:
            edge = self.edge_id_to_edge_mapping[edge_id]
            edge.shift_cars_up()
            print(edge.id, edge.queue)

    # def calculate_all_paths(self, start_node, end_node, current_path=[]):
    #     all_paths = []
    #     if not current_path:  # TODO:  this is clunky, fix later
    #         current_path = [start_node]
    #     # current_route_length = 0   # not used in V1
    #     for neighbour in start_node.node_id_neighbours:  # not considering length yet
    #         if neighbour not in current_path:
    #             current_path.append(neighbour)
    #             if neighbour == end_node:
    #                 print("route complete") 
    #                 all_paths.append(current_path)
                

      

class Node():
    def __init__(self, config) -> None:
        self.id = config["node_ID"]
        self.inbound_edge_id_to_edge_mapping = collections.defaultdict(lambda: None)
        self.outbound_edge_id_to_edge_mapping = collections.defaultdict(lambda: None) 
        self.pre_loaded_cars = []
        self.cars_exiting_network = []  # cars that completed routes at this node

    def add_pre_load_car(self, car):   # rename accurately later
        # some logic to check if it's even possible?
        # maybe delete and replace with direct edge placement instead
        self.pre_loaded_cars.append(car)
    
    def check_outbound_opening(self, outbound_edge):
        '''see if the first position is occupied.  If not, opening possible'''
        if not outbound_edge:
            return False 
            # exception needed:  car cannot move as intended, see if recalculation possible
        return outbound_edge.has_space_for_new_car(0)

    def check_inbound_car_waiting(self, inbound_edge):
        '''see if car in last position, if so return True'''
        return inbound_edge.has_car_waiting_to_leave()

    def get_car_to_move(self, inbound_edge):
        return inbound_edge.get_car_waiting_to_leave()   # bounded deque automaticallly discards extra later

    def node_tick(self):
        # this block handles loading new cars:
        if self.pre_loaded_cars != []:
            car_to_add = self.pre_loaded_cars.pop()  # TODO: handle all new cars (for loop)
            next_edge_id = car_to_add.get_next_edge_id()
            if next_edge_id != None:
                next_edge = self.outbound_edge_id_to_edge_mapping[next_edge_id]
                if not next_edge:
                    # exception needed:  car cannot move as intended, see if recalculation possible
                    raise Exception("that edge does not exist")
                elif next_edge.has_space_for_new_car(0):
                    print(next_edge.id, "has potential space for a new car")
                    if not next_edge.pre_loaded_cars[0]:  # if no cars in wait -- TODO:  set up function in car,
                        # print("We are adding a car!")
                        next_edge.pre_loaded_cars.append(car_to_add.id)
                        print (next_edge.id, "incoming queue:", next_edge.pre_loaded_cars)
                        # next_edge.pre_loaded_cars.append(None)   # clear waiting queue

                return

        # if no new cars loaded at this node, check/move inbound cars:       
        for key in list(self.inbound_edge_id_to_edge_mapping.keys()):
            inbound_edge = self.inbound_edge_id_to_edge_mapping[key]
            # TODO: need random shuffle on inbound edge order
            if inbound_edge.has_car_waiting_to_leave():
                print("There is a car waitng to leave edge", inbound_edge.id)
                car_to_move = inbound_edge.get_car_waiting_to_leave()
                print(car_to_move)

                if car_to_move == [None]:   # handle list error ==> FIX LATER
                    continue
               
                elif car_to_move.get_terminal_point() == self.id:     # path complete
                    self.cars_exiting_network.append(car_to_move)  # delete car from network / store trip complete
                    print("Car", car_to_move, "has reached its destination")
                    continue

                # check if outbound possible:
                next_edge_id = car_to_move.get_next_edge_id()
                if next_edge_id != None:
                    next_edge = self.outbound_edge_id_to_edge_mapping[next_edge_id]
                    if not next_edge:
                        # exception needed:  car cannot move as intended, see if recalculation possible
                        raise Exception("That edge does not exist")
                    if next_edge.has_space_for_new_car(0):
                        if not next_edge.pre_loaded_cars[0]:  # if no cars in wait -- TODO:  set up function in car,
                            next_edge.pre_loaded_cars.append(car_to_move)
                            print(car_to_move, "will advance to edge", next_edge)   # clear waiting queue
                            next_edge.open_space_at_end = True    # flag that all cars can proceed
                        else:
                            print(next_edge, "already has cars waiting to load - car will not exit")   # clear waiting queue
                    else:
                        print("There is no space for this car. ")
                    # TODO: add +1 to car_on_network_time ==> use to calculate delays ==> VERSION 2
                else:
                    print("This car has no path left")



class Edge():
    def __init__(self, config) -> None:
        self.id = config["edge_ID"]
        self.start_node = config["start_node"]
        self.end_node = config["end_node"]
        self.length = config["edge_length"]
        self.queue = collections.deque([None] * self.length, maxlen=self.length)
        self.pre_loaded_cars = collections.deque([None], maxlen=1)  # FOR NOW:  assume only one car can enter at a time
        self.open_space_at_end = False  # Toggle in node_tick if car leaves edge

    def has_space_for_new_car(self, spot_index):
        return False if self.queue[spot_index] else True
    def has_car_waiting_to_leave(self):
        return True if self.queue[-1] else False
    def get_car_waiting_to_leave(self):
        car = self.queue[-1]
        self.queue[-1] = None
        return car
    
    def shift_cars_up(self):
        """Shift all cars up by one position
        First check if we have any newcomers"""
        car = self.pre_loaded_cars[0]
        if car:
            self.pre_loaded_cars[0] = None
            self.queue.appendleft(car)      # This is expensive!
            self.open_space_at_end = False  # ensure flag is back to false
        elif self.open_space_at_end == True:
            self.queue.rotate()
            self.open_space_at_end = False  # ensure flag is back to false
        else:         # procedurally go through edge and advance any cars where a NULL is present
            new_edge_queue = collections.deque()
            null_counter = 0            # for appending Nones at end
            adjacent_null_counter = 0   # for ensuring cars only advance 1 stage
            for i in range(self.length):
                spot = (-1)*(i+1)  # back indexing starts at -1
                car_value = self.queue[spot]
                if car_value:
                    new_edge_queue.appendleft(car_value)
                elif adjacent_null_counter > 0:
                    new_edge_queue.appendleft(car_value)
                    null_counter += 1
                    adjacent_null_counter = 0
                else:
                    adjacent_null_counter = 1
            new_edge_queue.append(null_counter * [None])   # this is appending a list of everything.... fix later
            self.queue = new_edge_queue
            self.open_space_at_end = False  # ensure flag is back to false
            

        # self.queue.appendleft(None)  # bounded deque automaticallly discards last element


class Car():
    def __init__(self, config) -> None:
        self.id = config["car_id"]
        self.start_node = config["start_node"]
        self.end_node = config["end_node"]
        self.upcoming_path = config["path"]   # replace with path calculation later
        self.edge_stack = copy.deepcopy(self.upcoming_path)
        self.edge_stack.reverse()   # reverse order for pop / next_edge function
        self.path_driven = []
    
    def get_next_edge_id(self):  # derive from path computation later
        if self.edge_stack == []:
            # We are at the end of our journey!
            return None
        next_edge = self.edge_stack.pop()
        self.path_driven.append(next_edge)    # don't actually do this til confirmed
        return next_edge

    def get_terminal_point(self):
        return self.end_node




if __name__ == "__main__":
    fh_network = open('network_config.json')
    imported_network = json.load(fh_network)

    fh_network.close()
    # print(imported_network)


    fh_car = open('car_config.json')
    imported_cars = json.load(fh_car)

    fh_car.close()
    # print(imported_cars)
    nm = NetworkManager(imported_network)
    tm = TrafficManager(nm, imported_cars)
    print(nm.node_id_neighbours())

    for i in range(8):
        tm.tick()




# todo
    
