class HashTable:
    """
    The HashTable class is a standard hash table used to hold the values for the package objects.
    The input is a list, and then uses the size of that list to determine the size of the hashtable.
    """
    def __init__(self, hash_list):
        """
        Big O = O(N)
        ------------
        Initializes a table the size of the inputted list
        """
        self.MAX_SIZE = len(hash_list) + 1
        self.table = []
        for i in range(self.MAX_SIZE):
            self.table.append(None)

    def add(self, key, item):
        """
        Big O = O(1)
        ------------
        Adds an object to the hash table based upon the key
        """
        bucket = hash(key) % self.MAX_SIZE
        self.table[bucket] = item

    def search(self, key):
        """
        Big O = O(1)
        ------------
        Searches the Hash Table for a key value
        """
        if key > self.MAX_SIZE:
            return None
        bucket = hash(key) % self.MAX_SIZE
        if self.table[bucket] is not None:
            return self.table[bucket]
        else:
            return None

    def showAll(self):
        """
        Big O = O(N)
        ------------
        Prints out each item in the hash table.
        """
        for item in self.table:
            if item is not None:
                print(item)
                print()

    def remove(self, key):
        """
        Big O = O(1)
        ------------
        Removes an object based off of it's key if it exists
        else, returns none
        """
        bucket = hash(key) % self.MAX_SIZE
        if self.table[bucket] is not None:
            self.table[bucket] = None
        else:
            return None
