
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

    def BFS(self):
        # if this returns an empty list, there is no path
        visited = [False]*len(self.vertex_names)
        path = [-1]*len(self.vertex_names)

        queue = []

        source = self.source
        sink = self.sink
        queue.append(source)
        visited[source] = True

        while queue:
            u = queue.pop(0)

            for i in range(len(self.ad_matrix[u])):
                if visited[i] == False and self.ad_matrix[u][i][0] > 0:
                    queue.append(i)
                    visited[i] = True
                    path[i] = u
                    if i == sink:
                        return path
        return []
    
    def FordFulkerson(self):
        max_flow = 0 # There is no flow initially
        matrix = self.ad_matrix
        # Augment the flow while there is path from source to sink
        path = self.BFS()
        while path:

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = self.sink
            while(s !=  self.source):
                path_flow = min (path_flow, matrix[path[s]][s][0])
                s = path[s]
 
            # Add path flow to overall flow
            max_flow +=  path_flow
 
            # update residual capacities of the edges and reverse edges
            # along the path
            v = self.sink
            while(v !=  self.source):
                u = path[v]
                matrix[u][v][0] -= path_flow
                matrix[v][u][0] += path_flow
                v = path[v]
            path = self.BFS()        
        return max_flow, matrix