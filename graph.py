
class Graph:
    def __init__(self):
        self.ad_matrix = []
        self.source = 0
        self.sink = 1
        self.vertex_names = ['S', 'T']
        for v in range(2):
            self.ad_matrix.append([[0,0] for i in range(2)])
        self.original_edges = []
    
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
        self.original_edges.append([origin, destination])
        self.ad_matrix[origin][destination][0] = capacity
        self.ad_matrix[origin][destination][1] = minimum_flow

    def print_matrix(self):
        print(self.vertex_names)
        for i in range(len(self.ad_matrix)):
            print(self.vertex_names[i], self.ad_matrix[i])

    def add_matrix(self, matrix):
        #test only
        self.ad_matrix = matrix
    
    def set_source_sink(self, source, sink):
        #test only
        self.source = source
        self.sink = sink

    def add_vertex_names(self, names):
        #test only
        self.vertex_names = names

    def BFS(self, matrix):
        # if this returns an empty list, there is no path
        visited = [False]*len(matrix)
        path = [-1]*len(matrix)

        queue = []

        source = self.source
        sink = self.sink
        queue.append(source)
        visited[source] = True

        while queue:
            u = queue.pop(0)

            for i in range(len(matrix[u])):
                if visited[i] == False and matrix[u][i][0] > 0:
                    queue.append(i)
                    visited[i] = True
                    path[i] = u
                    if i == sink:
                        return path
        return []
    
    def FordFulkerson(self):
        return self._FordFulkerson(self.ad_matrix)
    
    def _FordFulkerson(self, matrix):
        max_flow = 0
        path = self.BFS(matrix)
        while path:
            path_flow = float("Inf")
            s = self.sink
            while(s !=  self.source):
                path_flow = min(path_flow, matrix[path[s]][s][0])
                s = path[s]
 
            max_flow +=  path_flow
            v = self.sink
            while(v !=  self.source):
                u = path[v]
                matrix[u][v][0] -= path_flow
                matrix[v][u][0] += path_flow
                v = path[v]
            path = self.BFS(matrix)        
        return max_flow, matrix
    
    def sum_lower_bound(self):
        matrix = self.ad_matrix
        sum = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                sum += matrix[i][j][1]
        return sum
    
    def valid_flow(self):
        produce_vector = [0]*len(self.vertex_names) # how much each vertex produces or demands
        matrix = self.ad_matrix #get adjency matrix
        for i in range(len(self.vertex_names)): #convert lower bound edge to node demand and production
            for j in range(len(self.vertex_names)):
                produce_vector[i] -= matrix[j][i][1]
                produce_vector[j] += matrix[j][i][1]
                matrix[j][i][0] -= matrix[j][i][1] #substract lower bound from capacity
        
        matrix[self.sink][self.source] = [float("Inf"), 0] #add edge from sink to source with infinite capacity

        #add new super source and super sink
        super_source = len(self.vertex_names) 
        super_sink = len(self.vertex_names) + 1
        matrix.append([[0,0] for i in range(len(self.vertex_names)+2)])
        matrix.append([[0,0] for i in range(len(self.vertex_names)+2)])
        for i in range(len(self.vertex_names)):
            matrix[i].append([0,0])
            matrix[i].append([0,0])
        
        #add production and demand edges
        for i in range(len(produce_vector)):
            produced = produce_vector[i]
            if produced < 0:
                matrix[super_source][i][0] = -produced
            elif produced > 0:
                matrix[i][super_sink][0] = produced
        
        #get valid flow from ford fulkerson
        max_flow, valid_matrix = self._FordFulkerson(matrix)

        L = self.sum_lower_bound()
        #check if valid flow is possible
        super_source_flow = 0
        for i in range(len(self.vertex_names)+2):
            super_source_flow += valid_matrix[super_source][i][0]
        if super_source_flow != L:
            return False, []
        return True, valid_matrix

        