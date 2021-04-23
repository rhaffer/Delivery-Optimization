import csv
from dataStructures.package import Package
from dataStructures.graph import Vertex


def load_packages_from_csv():
    """
    Big O = O(N)
    ------------
    Loads each line from the Packages.csv into a Package object.
    Returns a list of all package objects from the CSV
    """
    objects = []
    with open('./refs/packages.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            objects.append(Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    return objects


def load_distances_from_csv():
    """
    Big O = O(N^2)
    --------------
    Loads the distances from the distance table and recreates the full
    matrix.
    """
    with open('./refs/distances.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        reader = list(reader)
    for row in range(len(reader)):
        for column in range(len(reader[row])):
            distance = reader[row][column]
            if distance == '':
                distance = reader[column][row]
                reader[row][column] = distance
    return reader


def load_locations_from_csv():
    """
    Big O = O(N)
    ------------
    Loads locations from the location CSV
    """
    with open('./refs/locations.csv', newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)
        location_result = list(reader)
        location_list = []
        for row in location_result:
            result = row[0].split('\n')
            result = result[0][1:]
            if "South" in result:
                result = result.replace("South", "S")
            if "North" in result:
                result = result.replace("North", "N")
            if "East" in result:
                result = result.replace("East", "E")
            if "West" in result:
                result = result.replace("West", "W")

            location_list.append(result)
    return location_list


def create_vertices(lst):
    """
    Big O = O(N)
    ------------
    Creates a list of vertices from a list of points
    """
    vertices = []
    for item in lst:
        vertices.append(Vertex(item))
    return vertices


def load_Truck(trucks, hashTable):
    """
    Big O = O(N)
    The load truck function takes in a list of trucks and a hashtable containing all of the
    packages and loads the trucks according to the guidelines specified by the rubric. Additional
    packages are loaded in order to meet time delivery deadlines as specified by the rubric. All
    subsequent packages are loaded incrementally into any empty truck starting with Truck 1 and ending with
    Truck 3.
    """
    truck1_list = [13, 14, 15, 16, 19, 20, 30, 34, 40]
    truck2_list = [29, 31, 36, 37, 38, 3]
    truck3_list = [6, 9, 25, 28]
    for truck in trucks:
        if truck.getTruckID() == 1:
            for package in truck1_list:
                package = hashTable.search(package)
                truck.addPackage(package)
                package.setStatus("IN-TRANSIT")
                package.setTruck(truck.getTruckID())
        if truck.getTruckID() == 2:
            for package in truck2_list:
                package = hashTable.search(package)
                truck.addPackage(package)
                package.setStatus("IN-TRANSIT")
                package.setTruck(truck.getTruckID())
        if truck.getTruckID() == 3:
            for package in truck3_list:
                package = hashTable.search(package)
                truck.addPackage(package)
                package.setStatus("IN-TRANSIT")
                package.setTruck(truck.getTruckID())
    for truck in trucks:
        for i in range(1, len(hashTable.table)):
            if len(truck.packages) < truck.MAX_PACKAGES:
                package = hashTable.search(i)
                if package.getTruck() is None:
                    truck.addPackage(package)
                    package.setStatus("IN-TRANSIT")
                    package.setTruck(truck.getTruckID())
