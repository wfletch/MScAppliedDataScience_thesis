import json

class TrafficManager():
    def __init__(self, network_manager):
        self.nm = network_manager


class NetworkManager():
    def __init__(self, network_config, car_config):
        self.node_list = []
        self.edge_list = []

        for node_entry in network_config["node_list"]:
            self.node_list.append(Node(node_entry))
        print(self.node_list)

        for edge_entry in network_config["edge_list"]:
            self.edge_list.append(Edge(edge_entry))
        print(self.edge_list)

class Node():
    def __init__(self, config) -> None:
        self.id = config["node_ID"]

class Edge():
    def __init__(self, config) -> None:
        self.id = config["edge_ID"]
        self.start_node = config["start_node"]
        self.end_node = config["end_node"]

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


    