import json

class TrafficManager():
    def __init__(self, network_manager):
        self.nm = network_manager

    def tick():
        pass


class NetworkManager():
    def __init__(self, network_config, car_config):
        self.node_id_to_node_mapping = {}
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




class Node():
    def __init__(self, config) -> None:
        self.id = config["node_ID"]
        self.inbound_edge_id_to_edge_mapping = {}
        self.outbound_edge_id_to_edge_mapping = {}

class Edge():
    def __init__(self, config) -> None:
        self.id = config["edge_ID"]
        self.start_node = config["start_node"]
        self.end_node = config["end_node"]

class Car():
    def __init__(self, config) -> None:
        self.id = config["car_ID"]
        self.start_node = config["start_node"]
        self.end_node = config["end_node"]
        self.path = config["path"]


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


    