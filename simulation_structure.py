import json

if __name__ == "__main__":
    fh_network = open('network_config.json')
    imported_network = json.load(fh_network)

    fh_network.close()
    print(imported_network)


    fh_car = open('car_config.json')
    imported_cars = json.load(fh_car)

    fh_car.close()
    print(imported_cars)






# class node():


# class edge():

# class network_manager():





# class car():








class traffic_manager():
    def __init__(self):
        pass

    def move():
        pass


    