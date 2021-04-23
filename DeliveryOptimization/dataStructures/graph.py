class Vertex:
    """
    Creates the adjacent vertex objects.
    Vertex labels are generated from locations.csv
    Taken from course material.
    """
    def __init__(self, label):
        self.label = label

    """
    Big O = O(1)
    ------------
    Getters and Setters for vertex class
    """
    def getLabel(self):
        return self.label

    def setLabel(self, label):
        self.label = label


class Graph:
    """
    Creates a graph data structure from the location data.
    Each weighted edge comes from distances.csv
    Taken from course material.
    """
    def __init__(self):
        """
        Big O = O(1)
        ------------
        Creates new dictionaries for the adjacency and edge_weights list
        """
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        """
        Big O = O(1)
        ------------
        Creates new list at the index in adjacency_list where the new_vertex is located
        """
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        """
        Big O = O(1)
        ------------
        This adds the directed edges onto the graph
        """
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        """
        Big O = O(1)
        ------------
        This adds the undirected edges onto the graph
        """
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def find_vertex_by_label(self, label):
        """
        Big O = O(N^2)
        --------------
        This was used in order to make it easier for me to find
        vertices by their labels throughout the program.
        """
        for point in self.edge_weights:
            for item in point:
                if item.getLabel() == label:
                    return item

    def getDistance(self, from_vertex, to_vertex):
        """
        Big O = O(N)
        This takes two labels (each from a corresponding vertex) and
        returns the edge weight (distance) of the two points
        """
        from_vertex = self.find_vertex_by_label(from_vertex)
        to_vertex = self.find_vertex_by_label(to_vertex)
        point = (from_vertex, to_vertex)
        if point in self.edge_weights:
            return self.edge_weights[point]
