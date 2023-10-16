from collections import defaultdict
import random
from threading import Thread

class Node:
    def __init__(self, name, neighbours=[]) -> None: # neighbours is a list of tuples: [(name, weight)]
        self.name = name
        self.neighbours = neighbours
    
    def get_name(self):
        return self.name
    
    def get_neighbours(self):
        return self.neighbours

    def add_neighbour(self, neighbour, w): # neighbour is string
        self.neighbours.append((neighbour, w))

    def remove_neighbour(self, neighbour):
        for n, w in self.neighbours:
            if n == neighbour:
                self.neighbours.remove((n, w))
                break

class Graph:
    def __init__(self, connections) -> None: # get list of nodes from dict of connetions
        self.nodes = []
        for n in connections.keys():
            neighbours = []
            for each in connections[n]:
                neighbours.append([each[0], each[1], 1, 1/each[1]])
            self.nodes.append(Node(n, neighbours))
    
    def get_node_by_name(self, name) -> Node:
        for n in self.nodes:
            if n.get_name() == name:
                return n
    
    def Dijkstra(self, start):
        D = {}
        V = {}
        P = {}
        for n in self.nodes:
            D[n.get_name()] = 10000
            V[n.get_name()] = False
            P[n.get_name()] = None
        D[start] = 0
        
        for n in self.nodes:
            for key in D.keys():
                if not V[key]:
                    cur_min_node = key
                    break
            for key in D.keys():
                if not V[key]:
                    if D[cur_min_node] > D[key]:
                        cur_min_node = key

            V[cur_min_node] = True
            node = self.get_node_by_name(cur_min_node)

            for to, weight, _, _ in node.get_neighbours():
                if D[to] > D[cur_min_node] + weight:
                    D[to] = D[cur_min_node] + weight
                    P[to] = cur_min_node
        return D, P
    
    def find_path(self, start, finish):
        D, P = self.Dijkstra(start)
        cur_point = finish
        path = []
        while cur_point != start:
            path.append(cur_point)
            cur_point = P[cur_point]
        path.append(start)
        path.reverse()
        return D[finish], path
    

    def thread_ant(self):
        threads = [None] * len(self.nodes)
        for i in range(len(self.nodes)):
            thread = Thread(target=self.tsp, args=(self.nodes[i].get_name(), threads, i))
            thread.start()
            thread.join()
        min_dist = 10000
        min_path = []
        for t in threads:
            if t[0] < min_dist:
                min_dist = t[0]
                min_path = t[1]
        return min_dist, min_path

    def tsp(self, start, threads=[], thread_index=0):
        evaporation = 0
        visited = []
        dist = 0
        mins = {}
        paths = {}
        for node in self.nodes:
            paths[node.get_name()] = []
            mins[node.get_name()] = 100000
        for i in range(100000):
            # visited = [self.nodes[random.randint(0, len(self.nodes)-1)].get_name()]
            visited = [start]
            dist = 0
            fail = False
            while len(visited) < len(self.nodes):
                node = self.get_node_by_name(visited[-1])
                choice = random.random()
                sum = 0
                probs = []
                count_neighbours = 0
                for other, weight, t, n in node.get_neighbours():
                    if other in visited:
                        count_neighbours += 1
                        continue
                    sum += t*n
                    probs.append([other, t*n, weight])
                if len(node.neighbours) == count_neighbours:
                    fail = True
                    break
                for j in range(len(probs)):
                    probs[j][1] /= sum
                    if j > 0:
                        probs[j][1] += probs[j-1][1]
                for other, tn, w in probs:
                    if choice < tn:
                        visited.append(other)
                        dist += w
                        break
            if fail:
                continue
            for j in range(len(visited)-1):
                node = self.get_node_by_name(visited[j])
                for each in node.get_neighbours():
                    if each[0] == visited[j+1]:
                        each[2] = (1-evaporation) * each[2] + 1/dist
            if mins[visited[0]] > dist:
                mins[visited[0]] = dist
                paths[visited[0]] = visited
        node = 0
        dist = 10000
        path = []
        for each in mins.keys():
            if mins[each] < dist:
                node = each
                dist = mins[each]
                path = paths[each]
        # return dist, path
        threads[thread_index] = (dist, path)