from dataStructures.graph import Graph
from dataStructures.hashTable import HashTable
from dataStructures.trucks import Truck
from helperFunctions.functions import *
import datetime


class Simulation:
    """
    The Simulation class brings all of the data structures and algorithms together into a CLI based
    format. The user inputs various options and the program will run according to the option selected.
    """
    def __init__(self):
        self.running = True
        self.simulation_ran = False
        self.time_stamp_ran = False
        """--------------------------------------------------------------------------------
        Loads the package, distance and location data from the CSVs file located in /refs |
        --------------------------------------------------------------------------------"""
        self.packages = load_packages_from_csv()
        self.distances = load_distances_from_csv()
        self.locations = load_locations_from_csv()
        """--------------------------------------------
        Initializes the Packages Hashtable            |
        Big O = O(N)                                  |
        --------------------------------------------"""
        self.hashTable = HashTable(self.packages)
        for package in self.packages:
            self.hashTable.add(package.packageID, package)
        """---------------------------------------------------------------------------------
        Creates and initializes the Graph that holds the location and distance information |
        Big O --                                                                           |
            create_vertexes()   = O(N)                                                     |
            Adding vertexes     = O(N)                                                     |
            Adding edge weights = O(N^2)                                                   |
        ---------------------------------------------------------------------------------"""
        self.graph = Graph()
        graph_vertices = create_vertices(self.locations)
        for vertex in graph_vertices:
            self.graph.add_vertex(vertex)

        for distance in self.distances:
            for element in distance:
                if element != '':
                    row_index = self.distances.index(distance)
                    col_index = distance.index(element)
                    self.graph.add_undirected_edge(graph_vertices[row_index], graph_vertices[col_index], float(element))

        """------------------------------------------------------------------------|
        Initializes the trucks. Truck 2's start time is offset in order to meet    |
        deadlines specified by the rubric. Trucks are then loaded and sorted.      |
        Time complexity of each algorithm can be found in dataStructures/trucks.py |
        -------------------------------------------------------------------------"""
        self.t1 = Truck(1)
        self.t2 = Truck(2, "9:00")
        self.t3 = Truck(3)
        self.trucks = [self.t1, self.t2, self.t3]
        load_Truck(self.trucks, self.hashTable)

        for truck in self.trucks:
            truck.sort_packages(self.graph)

    def run(self):
        """
        Big O = O(N^2)
        ------------
        The run function provides the user with the options to run the program.
        The program must be reran anytime a delivery is made. Packages can be looked up before,
        during (timestamped) or after delivery.
        """
        while self.running:
            menu = {'1': "Run Simulation", '2': "Retrieve Timestamp", '3': "Lookup Package", '4': "Show All Packages",
                    '5': "Exit"}
            options = menu.keys()
            for entry in options:
                print(entry, menu[entry])
            selection = input("\nPlease Select an Option: \n").strip()
            if selection == '1':
                self.run_simulation()
            elif selection == '2':
                self.run_time_stamp()
            elif selection == '3':
                self.lookup_package()
            elif selection == '4':
                self.show_all_packages()
            elif selection == '5':
                self.running = False
            else:
                print("Option not available. Please select an option from available choices." + "\n")

    def run_simulation(self):
        """
        Big O = O(N)
        ------------
        Run_simulation runs the entire simulation from start to finish. Truck 1 is delivered first, then truck 2.
        Depending on which truck finishes first, truck 3's time is started.
        This function also allows for a full detailed breakdown on the path of each truck, the start and end times,
        as well as the total distance traveled.
        """
        if not self.simulation_ran and not self.time_stamp_ran:
            self.t1.deliver_packages(self.graph)
            self.t2.deliver_packages(self.graph)
            if self.t1.finished or self.t2.finished:
                if self.t1.getEndTime() <= self.t2.getEndTime():
                    self.t3.setStartTime(self.t1.getEndTime().strftime("%H:%M"))
                    self.t3.deliver_packages(self.graph)
                else:
                    self.t3.setStartTime(self.t2.getEndTime().strftime("%H:%M"))
                    self.t3.deliver_packages(self.graph)
            print()
            print("Simulation ran. Please select option 3 or 4 to see Package status.\n")
            print("Truck 1 Path: " + self.t1.path)
            print("Truck 1 Start Time: " + str(self.t1.start_time.time()))
            print("Truck 1 End Time: " + str(self.t1.end_time.time()))
            print("Truck 1 Distance: " + str(round(self.t1.total_distance, 2)) + "\n")
            print("Truck 2 Path: " + self.t2.path)
            print("Truck 2 Start Time: " + str(self.t2.start_time.time()))
            print("Truck 2 End Time: " + str(self.t2.end_time.time()))
            print("Truck 2 Distance: " + str(round(self.t2.total_distance, 2)) + "\n")
            print("Truck 3 Path: " + self.t3.path)
            print("Truck 3 Start Time: " + str(self.t3.start_time.time()))
            print("Truck 3 End Time: " + str(self.t3.end_time.time()))
            print("Truck 3 Distance: " + str(round(self.t3.total_distance, 2)) + "\n")

            print("Total Distance: " + str(round(self.t1.total_distance + self.t2.total_distance +
                                                 self.t3.total_distance, 2)))
            print("End Time: " + str(self.t3.end_time.time()) + "\n")
            self.simulation_ran = True
        else:
            print("Simulation already ran. Packages cannot be delivered twice!" + "\n")

    def run_time_stamp(self):
        """
        Big O = O(N)
        ------------
        Run_time_stamp allows for the user to input a specific time in the HH:MM format. The trucks are then delivered
        until that time stamp is reached. In order to see the package status, either
        lookup_package() or show_all_packages() must be called.
        """
        if not self.simulation_ran and not self.time_stamp_ran:
            time_stamp = input("Please enter a time in HH:MM format: ")
            try:
                datetime.datetime.strptime(time_stamp, '%H:%M')
                time_accepted = True
            except ValueError:
                print("\n" + time_stamp + " is not a valid entry. Please try again. \n")
                time_accepted = False
            if time_accepted:
                self.t1.deliver_packages(self.graph, stop_time=time_stamp)
                self.t2.deliver_packages(self.graph, stop_time=time_stamp)
                if self.t1.finished or self.t2.finished:
                    if self.t1.getEndTime() <= self.t2.getEndTime():
                        self.t3.setStartTime(self.t1.getEndTime().strftime("%H:%M"))
                        self.t3.deliver_packages(self.graph, stop_time=time_stamp)
                    else:
                        self.t3.setStartTime(self.t2.getEndTime().strftime("%H:%M"))
                        self.t3.deliver_packages(self.graph, stop_time=time_stamp)
                print()
                print("Timestamp Simulation ran. Please select option 3 or 4 to see Package status." + "\n")
                self.time_stamp_ran = True
        else:
            print("Simulation already ran. Packages cannot be delivered twice!" + "\n")

    def lookup_package(self):
        """
        Big O = O(1)
        ------------
        Lookup_package uses the hashtable to search for a package by its package ID. All information regarding
        this package is then printed.
        """
        selection = int(input("Please enter a package ID: "))
        selection = self.hashTable.search(selection)
        if selection is None:
            print("\n Package not found! \n")
        else:
            print("\n", selection, "\n")

    def show_all_packages(self):
        """
        Big O = O(N)
        ------------
        Show_all_packages prints all package information contained within the Hashtable.
        """
        self.hashTable.showAll()
