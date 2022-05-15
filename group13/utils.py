from functools import lru_cache


class Graph():
    """ A data structure for Graph """

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        
    def edges(self):
        all_edges = []
        for key, adj_nodes in self.adjacency_list.items():
            all_edges += [(key, adj_node) for adj_node in adj_nodes]
        return all_edges 

def qsort(arr):
    if len(arr) <= 1:
        return arr
    else:
        return qsort([x for x in arr[1:] if x < arr[0]]) + [arr[0]] + qsort([x for x in arr[1:] if x >= arr[0]])

import queue

def bfs(graph, node): #function for BFS
#    print('BFS of adjacency list with root: {}'.format(node))
    queue = []     #Initialize a queue
    visited = []
    lvl_container = {}
    marked = []
    visited.append(node)
    queue.append(node)
    l = 1
    while queue:        # Creating loop to visit each node
        m = queue.pop(0) 
        lvl_container[l] = []
        for neighbour in graph[m]:
            if neighbour not in visited:
                if m not in marked:
                    marked.append(m)
#                print(str(m)+' has neighbour: '+str(neighbour)+' (level: {}) '.format(l))
                lvl_container[l].append(neighbour)
                lvl_container[l] = qsort(lvl_container[l])
                visited.append(neighbour)
                queue.append(neighbour)
        if lvl_container[l] == '' or l==10:
            break
        if graph[m] != [] and m in marked:
            l += 1
    for i in range(l,11):
        lvl_container[i] = []
    return lvl_container

'''
def bfs_old(s):
    marked = []
    q = queue.Queue()
    marked.append(s)
    q.put(s)
    while q != []:
        print(q)
        break
# Utility bfs method to fill distance
# vector and returns most distant
# marked node from node u
def bfsWithDistance(g, mark, u, dis):
    lastMarked = 0
    q = queue.Queue()
 
    # push node u in queue and initialize
    # its distance as 0
    q.put(u)
    dis[u] = 0
 
    # loop until all nodes are processed
    while (not q.empty()):
        u = q.get()
         
        # if node is marked, update
        # lastMarked variable
        if (mark[u]):
            lastMarked = u
 
        # loop over all neighbors of u and
        # update their distance before
        # pushing in queue
        for i in range(len(g[u])):
            v = g[u][i]
             
            # if not given value already
            if (dis[v] == -1):
                dis[v] = dis[u] + 1
                q.put(v)
                 
    # return last updated marked value
    return lastMarked

# method returns count of nodes which
# are in K-distance range from marked nodes
def nodesKDistanceFromMarked(edges, V, marked, N, K):
    
    # vertices in a tree are one
    # more than number of edges
    V = V + 1
    g = [[] for i in range(V)]
 
    # fill vector for graph
    u, v = 0, 0
    for i in range(V - 1):
        u = edges[i][0]
        v = edges[i][1]
 
        g[u].append(v)
        g[v].append(u)
 
    # fill boolean array mark from
    # marked array
    mark = [False] * V
    for i in range(N):
        mark[marked[i]] = True
 
    # vectors to store distances
    tmp = [-1] * V
    dl = [-1] * V
    dr = [-1] * V
 
    # first bfs(from any random node)
    # to get one distant marked node
    u = bfsWithDistance(g, mark, 0, tmp)
 
    # second bfs to get other distant
    # marked node and also dl is filled
    # with distances from first chosen
    # marked node
    u = bfsWithDistance(g, mark, u, dl)
 
    # third bfs to fill dr by distances
    # from second chosen marked node
    bfsWithDistance(g, mark, u, dr)
 
    res = 0
     
    # loop over all nodes
    for i in range(V):
         
        # increase res by 1, if current node
        # has distance less than K from both
        # extreme nodes
        if (dl[i] <= K and dr[i] <= K):
            res += 1
    return res

if __name__ == '__main__':
 
    edges = [[1, 0], [0, 3], [0, 8],
             [2, 3], [3, 5], [3, 6],
             [3, 7], [4, 5], [5, 9]]
    V = len(edges)
     
    marked = [1, 2, 4]
    N = len(marked)
 
    K = 3
    print(nodesKDistanceFromMarked(edges, V,
                                   marked, N, K))


def bfs_exercise(visited, graph, node):
    # NOTE: this is not the full BFS algorithm,
    # it is just a sketch to show the queue execution
    visited.append(node)
    queue.append(node)

    while queue:
        print("Queue:", queue)
        s = queue.pop(0) 

        print("Extract: ", s) 
        print("Neighbours:", graph[s])
        print("--")
        for neighbour in graph[s]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

def bfs(node):
    visited.append(node)
    queue.append(node)'''