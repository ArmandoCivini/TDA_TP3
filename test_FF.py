from graph import Graph

def test_FF():
    graph = [[0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0]]

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            graph[i][j] = [graph[i][j], 0]

    g = Graph()
    g.add_matrix(graph)
    g.set_source_sink(0, 5)
    g.add_vertex_names(['S', 'A', 'B', 'C', 'D', 'T'])
    print(g.FordFulkerson())

def print_matrix(vertex_names, ad_matrix):
    print(vertex_names)
    for i in range(len(ad_matrix)):
        print(vertex_names[i], ad_matrix[i])

def test_valid_flow():
    graph = [[0, 4, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 5],
            [0, 0, 0, 0]]

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            graph[i][j] = [graph[i][j], 0]
    
    graph[0][1][1] = 1

    g = Graph()
    g.add_matrix(graph)
    g.set_source_sink(0, 3)
    g.add_vertex_names(['S', 'A', 'B', 'T'])
    valid, matrix = g.valid_flow()
    print(valid)
    if valid: print_matrix(['S', 'A', 'B', 'T', 'S*', 'T*'], matrix)

test_valid_flow()
# test_FF()