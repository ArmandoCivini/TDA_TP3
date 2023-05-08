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

def test_valid_flow():
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
    print(g.valid_flow())

test_valid_flow()
# test_FF()