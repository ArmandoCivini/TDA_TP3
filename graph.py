
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
    
    def _add_og_edge(self, edge):
        self.original_edges.append(edge)

    def print_matrix(self):
        self._print_matrix(self.ad_matrix, self.vertex_names)

    def _print_matrix(self, matrix, names):
        print(names)
        for i in range(len(names)):
            print(names[i], matrix[i][:len(names)])

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

    def BFS(self, matrix, source, sink):
        # if this returns an empty list, there is no path
        visited = [False]*len(matrix)
        path = [-1]*len(matrix)

        queue = []

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
        return self._FordFulkerson(self.ad_matrix, self.sink, self.source)
    
    def _FordFulkerson(self, matrix, sink, source):
        max_flow = 0
        path = self.BFS(matrix, source, sink)
        while path:
            path_flow = float("Inf")
            s = sink
            while(s !=  source):
                path_flow = min(path_flow, matrix[path[s]][s][0])
                s = path[s]
 
            max_flow +=  path_flow
            v = sink
            while(v !=  source):
                u = path[v]
                matrix[u][v][0] -= path_flow
                matrix[v][u][0] += path_flow
                v = path[v]
            path = self.BFS(matrix, source, sink)        
        return max_flow, matrix
    
    def sum_lower_bound(self, produce_vector):
        sum = 0
        for value in produce_vector:
            if value > 0:
                sum += value
        return sum
    
    def create_produce_vector(self):
        produce_vector = [0]*len(self.vertex_names) # how much each vertex produces or demands
        matrix = self.ad_matrix #get adjency matrix
        for i in range(len(self.vertex_names)): #convert lower bound edge to node demand and production
            for j in range(len(self.vertex_names)):
                produce_vector[i] += matrix[i][j][1]
                produce_vector[j] -= matrix[i][j][1]
                matrix[i][j][0] -= matrix[i][j][1] #substract lower bound from capacity
        return produce_vector, matrix
    
    def valid_flow(self):
        produce_vector, matrix = self.create_produce_vector()
        print("produce vector:")
        print(produce_vector)
        # print("matrix:")
        # print(matrix)
        
        matrix[self.sink][self.source] = [float("inf"), 0] #add edge from sink to source with infinite capacity

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
        
        print("matrix:")
        self._print_matrix(matrix, self.vertex_names + ["S*", "T*"])
        #get valid flow from ford fulkerson
        max_flow, valid_matrix = self._FordFulkerson(matrix, super_sink, super_source)
        print("valid matrix:")
        self._print_matrix(valid_matrix, self.vertex_names + ["S*", "T*"])
        L = self.sum_lower_bound(produce_vector)
        #check if valid flow is possible
        super_source_flow = 0
        for i in range(len(self.vertex_names)+2):
            super_source_flow += valid_matrix[i][super_source][0]
        if super_source_flow != L:
            return False, []
        max_flow, valid_flow_complete = self.add_valid_flow(valid_matrix)
        return True, valid_flow_complete #TODO: return valid matrix
    
    def valid_flow_transform(self, valid_matrix):
        matrix = self.ad_matrix
        for edge in self.original_edges:
            i, j = edge[0], edge[1]
            matrix[i][j][0] -= valid_matrix[j][i][0]
            matrix[j][i][0] = valid_matrix[j][i][0] - matrix[i][j][1]
        return matrix
    
    def add_valid_flow(self, matrix):
        for edge in self.original_edges:
            i, j = edge[0], edge[1]
            print(matrix[i][j][1])
            matrix[j][i][0] += matrix[i][j][1]
        max_flow = 0
        for i in range(len(matrix[self.sink])):
            max_flow += matrix[self.sink][i][0]
        return max_flow, matrix
    
    def reverse_flow(self, matrix):
        new_matrix = [[0 for i in range(len(self.vertex_names))] for j in range(len(self.vertex_names))]
        for edge in self.original_edges:
            i, j = edge[0], edge[1]
            new_matrix[i][j] = matrix[j][i][0]
        return new_matrix
    
    def clean_matrix(self, matrix):
        matrix.pop()
        matrix.pop()
        for i in range(len(matrix)):
            matrix[i].pop()
            matrix[i].pop()

    def max_flow(self):
        valid, valid_matrix = self.valid_flow()
        if not valid: return -1, []
        valid_matrix[self.sink][self.source] = [0,0]
        print("valid matrix")
        self._print_matrix(valid_matrix, self.vertex_names + ["S*", "T*"])
        transformed_matrix = self.valid_flow_transform(valid_matrix)
        print("after transform")
        self._print_matrix(transformed_matrix, self.vertex_names)
        max_flow, FF_matrix = self._FordFulkerson(transformed_matrix, self.sink, self.source)
        print("after FF")
        self._print_matrix(FF_matrix, self.vertex_names + ["S*", "T*"])
        max_flow, true_matrix = self.add_valid_flow(FF_matrix)
        final_matrix = self.reverse_flow(true_matrix)
        print("adding back the flow")
        self._print_matrix(true_matrix, self.vertex_names)
        return max_flow, final_matrix

        