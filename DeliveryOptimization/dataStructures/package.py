class Package:
    """
    The Package class is an object related to each package and holds the values for each package.
    These objects will then be placed into the HashTable object.
    """
    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline, mass, special_instructions):
        self.packageID = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zipcode
        self.delivery_deadline = delivery_deadline
        self.mass = float(mass)
        self.special_instructions = special_instructions
        self.status = "AT_HUB"
        self.truck = None
        self.delivery_time = ""
        self.replace_cardinal_directions()

    """
    Big O = O(1)
    ------------
    Below are the getters and setters for the Package class. 
    All getters and setters share the same complexity.
    """
    def setPackageID(self, packageID):
        self.packageID = packageID

    def getPackageID(self):
        return self.packageID

    def setAddress(self, address):
        self.address = address

    def getAddress(self):
        return self.address

    def setCity(self, city):
        self.city = city

    def getCity(self):
        return self.city

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setZip(self, zipcode):
        self.zip = zipcode

    def getDeliveryDeadline(self):
        return self.delivery_deadline

    def setDeliveryDeadline(self, deadline):
        self.delivery_deadline = deadline

    def getMass(self):
        return self.mass

    def setMass(self, mass):
        self.mass = mass

    def getSpecialInstructions(self):
        return self.special_instructions

    def setSpecialInstructions(self, instructions):
        self.special_instructions = instructions

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getTruck(self):
        return self.truck

    def setTruck(self, truck):
        self.truck = truck

    """
    Big O = O(N)
    ------------
    The replace cardinal directions function cleans up the data and ensure continuity between
    Package and Location/Distance information
    """
    def replace_cardinal_directions(self):
        if "North" in self.address:
            self.address = self.address.replace("North", "N")
        if "South" in self.address:
            self.address = self.address.replace("South", "S")
        if "East" in self.address:
            self.address = self.address.replace("East", "E")
        if "West" in self.address:
            self.address = self.address.replace("West", "W")

    def __str__(self):
        """
        Overriding the default str method for a class. Gives a format to print a Package object.
        """
        return f"""Package ID: {self.packageID}
Address: {self.address}
City: {self.city}
State: {self.state}
Zipcode: {self.zip}
Delivery Deadline: {self.delivery_deadline}
Mass: {self.mass}
Special Instructions: {self.special_instructions}
Status: {self.status}
Truck: {self.truck}
Delivered at: {self.delivery_time}"""
