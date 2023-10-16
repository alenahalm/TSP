from graph import Graph

connections = {
    1: [(2, 10), (3, 6), (4, 8)],
    2: [(4, 5), (7, 11)],
    3: [(5, 3)],
    4: [(3, 2), (5, 5), (6, 7), (7, 12)],
    5: [(6, 9), (9, 12)],
    6: [(8, 8), (9, 10)],
    7: [(6, 4), (8, 6)],
    8: [(9, 1)],
    9: []
}

# gr = Graph(connections)
# ds, ps = gr.find_path(1, 9)

# D, P = gr.Dijkstra(1)
# print(D)
# print(P)
# print('Distance', ds)
# print('Path', ps)

ant_graph = {
    'a': [('b', 3), ('f', 1)],
    'b': [('a', 3), ('c', 8), ('g', 3)],
    'c': [('b', 3), ('d', 1), ('g', 1)],
    'd': [('c', 8), ('f', 1)],
    'f': [('d', 3), ('a', 3)],
    'g': [('a', 3), ('b', 3), ('c', 3), ('d', 5), ('f', 4)]
}


graph = Graph(ant_graph)
import time
start_time = time.time()
distance, path = graph.thread_ant()
print("--- %s seconds ---" % (time.time() - start_time))
print("Shortest distance is", distance)
print("Path", path)