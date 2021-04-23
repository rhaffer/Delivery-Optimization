from datetime import datetime, timedelta


class Truck:
    """
    The Truck class holds the packages that are in transit.
    Each truck holds the amount of distance that that truck has traveled.
    """
    MAX_SPEED = 18
    MAX_PACKAGES = 16

    def __init__(self, truckID, start_time="8:00"):
        self.truckID = truckID
        self.packages = []
        self.currentLocation = "HUB"
        self.nextLocation = None
        self.total_distance = 0
        self.start_time = datetime.strptime(start_time, '%H:%M')
        self.current_time = self.start_time
        self.end_time = self.start_time
        self.finished = False
        self.path = "HUB"

    """
    Big O = O(1)
    ------------
    Getters and Setters for the truck class
    """
    def getTruckID(self):
        return self.truckID

    def setTruckID(self, truck_id):
        self.truckID = truck_id

    def getPackages(self):
        return self.packages

    def addPackage(self, package):
        self.packages.append(package)

    def getCurrentLocation(self):
        return self.currentLocation

    def setCurrentLocation(self, location):
        self.currentLocation = location

    def getNextLocation(self):
        return self.nextLocation

    def setNextLocation(self, location):
        self.nextLocation = location

    def setStartTime(self, time):
        self.start_time = datetime.strptime(time, "%H:%M")
        self.current_time = self.start_time

    def getStartTime(self):
        return self.start_time.time()

    def getCurrentTime(self):
        return self.current_time.time()

    def getEndTime(self):
        return self.end_time.time()

    def sort_packages(self, graph):
        """
        Big O = O(N)
        ------------
        The sort packages function is a nearest neighbor algorithm that sorts
        the packages after being loaded into the truck. The algorithm begins by starting
        the current location at the Hub, and then checking each distance from the current location
        to the location of the next package and adds the shortest distance into a new list. The point with the
        shortest distance is removed from the packages list. The shortest distance point is then turned into
        the current location and the loop continues until there are no more packages in the trucks package
        list. This function then returns a list of packages sorted by the nearest neighbor.
        """
        current_location = "HUB"
        package_list = []
        while self.packages:
            distance_list = []
            for package in self.packages:
                distance = graph.getDistance(current_location, package.address)
                if package.delivery_deadline != "EOD":
                    distance = distance * 0.5
                if distance is None:
                    break
                distance_list.append((package, distance))
            shortest_distance = min(distance_list, key=lambda x: x[1])
            current_location = shortest_distance[0].address
            package_list.append(shortest_distance[0])
            self.packages.remove(shortest_distance[0])
        self.packages = package_list

    def deliver_packages(self, graph, stop_time='18:00'):
        """
        Big O = O(N)
        The deliver packages function delivers each package incrementally
        as they are in the truck.package list. Since the packages are sorted before they are
        delivered, this allows for an optimized delivery. The graph data structure is passed in
        in order to determine the distance between two points. Stop_time is used whenever
        a timestamp is requested by the user. The algorithm continues to deliver packages
        until the stop time is greater than or equal to the current time of that particular truck.
        Each truck then returns to the Hub.
        """
        index = 0
        stop_time = datetime.strptime(stop_time, "%H:%M")
        while not self.finished:
            for package in range(len(self.packages)):
                if stop_time >= self.current_time and index < len(self.packages):
                    self.setNextLocation(self.packages[index].getAddress())
                distance = graph.getDistance(self.currentLocation, self.nextLocation)
                time_to_deliver = distance / self.MAX_SPEED
                time_elapsed = self.current_time + timedelta(hours=time_to_deliver)
                if time_elapsed >= stop_time:
                    break
                else:
                    self.current_time = time_elapsed
                    self.setCurrentLocation(self.nextLocation)
                    self.total_distance += distance
                    self.packages[package].setStatus("DELIVERED")
                    self.packages[package].delivery_time = self.current_time.time()
                    self.path = self.path + " -> " + self.currentLocation
                    index += 1
            self.setNextLocation("HUB")
            distance = graph.getDistance(self.currentLocation, self.nextLocation)
            time_to_deliver = distance / self.MAX_SPEED
            time_elapsed = self.current_time + timedelta(hours=time_to_deliver)
            self.current_time = time_elapsed
            self.setCurrentLocation(self.nextLocation)
            self.total_distance += distance
            self.path = self.path + " -> " + self.currentLocation
            self.end_time = self.current_time
            self.finished = True
