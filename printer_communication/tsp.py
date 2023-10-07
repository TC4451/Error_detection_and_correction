
import numpy as np

MAX = np.iinfo(np.int32).max


def tsp_greedy(dist):
    num_cities = len(dist)
    path = [0]  # Start at city 0
    visited = set([0])
    current_city = 0
    dist[:,0] = MAX

    while len(visited) < num_cities:
        nearest_city = np.argmin(
            [dist[current_city][i] 
                for i in range(num_cities)])
        # print([dist[current_city][i] 
        #         for i in range(num_cities)])

        # print(nearest_city)
        path.append(nearest_city)
        visited.add(nearest_city)
        current_city = nearest_city
        # dist[nearest_city] = MAX
        dist[:,nearest_city] = MAX
        # print(visited)
    
    # path.append(0)  # Return to starting city
    # print(path)
    return path




from sys import maxsize
from itertools import permutations
V = 4
 
# implementation of traveling Salesman Problem
# def travellingSalesmanProblem(graph, s):
def travellingSalesmanProblem(graph):
 
    # store all vertex apart from source vertex
    vertex = []
    s = graph.shape[0]-1
    for i in range(V):
        if i != s:
            vertex.append(i)
 
    travel_path = []

    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    next_permutation=permutations(vertex)
    for i in next_permutation:
 
        # store current Path weight(cost)
        current_pathweight = 0
 
        # compute current path weight
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]
 
        # update minimum
        min_path = min(min_path, current_pathweight)

    print(min_path) 
    return min_path
 
 





def point_to_graph(points):
    connection_matrix = np.zeros((points.shape[0], points.shape[0]))
    for ii in range(points.shape[0]):
        for jj in range(ii):
            dist = np.linalg.norm(points[ii] - points[jj])
            connection_matrix[ii, jj] = dist
            connection_matrix[jj, ii] = dist
    print(connection_matrix)
    return connection_matrix



def vertex_to_graph(vertex):
    # from row to column
    connection_matrix = np.zeros((vertex.shape[0], vertex.shape[0]))
    for ii in range(vertex.shape[0]):
        for jj in range(vertex.shape[0]):
            dist = np.linalg.norm(vertex[ii,2:] - vertex[jj,:2])
            connection_matrix[ii, jj] = dist
    print(connection_matrix)
    return connection_matrix





if __name__ == '__main__':
    graph = np.array([[0, 10, 15, 20], [10, 0, 35, 25],
            [15, 35, 0, 30], [20, 25, 30, 0]])
    tsp_greedy(graph)
    # travellingSalesmanProblem(graph)

    
    pass