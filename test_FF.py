from graph import Graph
from graph_parser import graph_parser


def test_FF():
    graph = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0],
    ]

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            graph[i][j] = [graph[i][j], 0]

    g = Graph()
    g.add_matrix(graph)
    g.set_source_sink(0, 5)
    g.add_vertex_names(["S", "A", "B", "C", "D", "T"])
    g._add_og_edge([0, 1])
    g._add_og_edge([0, 2])
    g._add_og_edge([1, 2])
    g._add_og_edge([1, 3])
    g._add_og_edge([2, 1])
    g._add_og_edge([2, 4])
    g._add_og_edge([3, 2])
    g._add_og_edge([3, 5])
    g._add_og_edge([4, 3])
    g._add_og_edge([4, 5])
    max_flow, matrix = g.FordFulkerson()
    print(max_flow)
    print_matrix(["S", "A", "B", "C", "D", "T"], matrix)
    print_matrix(["S", "A", "B", "C", "D", "T"], g.reverse_flow(matrix))


def print_matrix(vertex_names, ad_matrix):
    print(vertex_names)
    for i in range(len(vertex_names)):
        print(vertex_names[i], ad_matrix[i][: len(vertex_names)])


def test_valid_flow1():
    g = graph_parser("example_video.txt")
    valid, matrix = g.valid_flow()
    print(valid)
    if not valid:
        return
    print_matrix(["S", "T", "A", "B", "C", "D", "S*", "T*"], matrix)
    print_matrix(["S", "T", "A", "B", "C", "D"], g.get_just_og_edges(matrix))


def test_valid_flow2():
    graph = [[0, 4, 0, 0], [0, 0, 2, 0], [0, 0, 0, 5], [0, 0, 0, 0]]

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            graph[i][j] = [graph[i][j], 0]

    graph[0][1][1] = 1  # change this number to 3 to see the invalid flow

    g = Graph()
    g.add_matrix(graph)
    g.set_source_sink(0, 3)
    g._add_og_edge([0, 1])
    g._add_og_edge([1, 2])
    g._add_og_edge([2, 3])
    g.add_vertex_names(["S", "A", "B", "T"])
    valid, matrix = g.valid_flow()
    print(valid)
    if not valid:
        return
    print_matrix(["S", "A", "B", "T", "S*", "T*"], matrix)
    print_matrix(["S", "A", "B", "T"], g.get_just_og_edges(matrix))


def test_max_flow():
    g = graph_parser("example_video.txt")
    print("MATRIZ OG")
    g.print_matrix()
    max_flow, matrix = g.max_flow()
    print(max_flow)
    if max_flow != -1:
        print_matrix(g.get_vertex_names(), matrix)


test_valid_flow1()
# test_valid_flow2()
# test_FF()
# test_max_flow()
