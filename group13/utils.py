def qsort(arr):
    if len(arr) <= 1:
        return arr
    else:
        return qsort([x for x in arr[1:] if x < arr[0]]) + [arr[0]] + qsort([x for x in arr[1:] if x >= arr[0]])

def bfs_adhoc(graph, node):
    queue = []     #Initialize a queue
    visited = []
    lvl_container = {}
    visited.append(node)
    queue.append(node)
    l = 1
    x = 0
    while l <= 10:
        try:
            m = queue.pop(0)
        except:
            return lvl_container 
        lvl_container[l] = []
        for neighbour in graph[m]:
            if neighbour not in visited:
#                print(str(m)+' has neighbour: '+str(neighbour)+' (level: {}) '.format(l))
                lvl_container[l].append(neighbour)
                visited.append(neighbour)
                queue.append(neighbour)
                x += 1
        lvl_container[l] = qsort(lvl_container[l])
        if x != 0:
            l += 1
            x = 0
    return lvl_container

def bfs(graph, node, lvl):
    queue = []     #Initialize a queue
    visited = []
    lvl_container = {}
    visited.append(node)
    queue.append(node)
    l = 1
    x = 0
    while l <= lvl:
        try:
            m = queue.pop(0)
        except:
            return []
        lvl_container[l] = []
        for neighbour in graph[m]:
            if neighbour not in visited:
#                print(str(m)+' has neighbour: '+str(neighbour)+' (level: {}) '.format(l))
                lvl_container[l].append(neighbour)
                visited.append(neighbour)
                queue.append(neighbour)
                x += 1
        if x != 0:
            l += 1
            x = 0
    return qsort(lvl_container[lvl])

def bfs2(graph, node, lvl):
    queue = [node]
    visited = [node]
    lvl_container = [node]
    lvl_container2 = []
    l = 0
    while l < lvl:
        if len(queue) == 0:
            return []
        lvl_container.pop(0)
        a = queue.pop(0)
        for i in graph[a]:
            if i not in visited:
                visited.append(i)
                queue.append(i)
                lvl_container2.append(i)
        if len(lvl_container) == 0:
            lvl_container = lvl_container2
            lvl_container2 = []
            l += 1    
    return qsort(lvl_container)

class Graph2:
    def __init__(self, adj):
 
        # No. of vertices
 
        # Pointer to an array containing
        # adjacency lists
        self.adj = adj
 
    # Function to return the number of
    # connected components in an undirected graph
    def NumberOfconnectedComponents(self):
        
        visited = {}
        # Mark all the vertices as not visited
        for i in self.adj.keys():
            visited[i] = False
         
        # To store the number of connected
        # components
        count = 0
         
        for v in self.adj.keys():
            if (visited[v] == False):
                self.DFS(v, visited)
                count += 1
                 
        return count
         
    def DFS(self, v, visited):
 
        # Mark the current node as visited
        visited[v] = True
 
        # Recur for all the vertices
        # adjacent to this vertex
        for i in self.adj[v]:
            if (not visited[i]):
                self.DFS(i, visited)

#if __name__ == '__main__':
#    print(bfs(adjacency_list, 'GOOGL', 2))