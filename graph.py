


class Graph:
    def __init__(self):
        self.ad_matrix = []
        self.source = 0
        self.sink = 1
        self.vertex_names = ['S', 'T']
        for v in range(2):
            self.ad_matrix.append([[0,0] for i in range(2)])
    
    def add_vertex(self, name):
        self.vertex_names.append(name)
        self.ad_matrix.append([[0,0] for i in range(len(self.vertex_names))])
        for i in range(len(self.vertex_names)-1):
            self.ad_matrix[i].append([0,0])

    def add_edge(self, name_origin, name_destination, capacity, minimum_flow):
        if name_origin not in self.vertex_names:
            self.add_vertex(name_origin)
        if name_destination not in self.vertex_names:
            self.add_vertex(name_destination)
        origin = self.vertex_names.index(name_origin)
        destination = self.vertex_names.index(name_destination)
        self.ad_matrix[origin][destination][0] = capacity
        self.ad_matrix[origin][destination][1] = minimum_flow

    def print_matrix(self):
        print(self.vertex_names)
        for i in range(len(self.ad_matrix)):
            print(self.vertex_names[i], self.ad_matrix[i])