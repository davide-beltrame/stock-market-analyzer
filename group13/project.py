#from math import expm1
#from platform import node
import gplot
from functools import lru_cache
#from collections import queue
#from matplotlib import pyplot as plt
try: # this is for running main.py
    import group13.utils
    from group13.utils import Graph, qsort, bfs
except: # this is for running directly project.py (for testing)
    import utils
    from utils import Graph, qsort, bfs

from queue import Queue

@lru_cache()
def prepare(filename : str, threshold : float):

    global new_container
    global adjacency_list
    stock_container = {}
    new_container = {}
    adjacency_list = {} 

    with open(filename,'r') as f:
        for line in f:
            line = line.replace('\n','')
            line = line.split(',')
            if line[0] not in stock_container:
                stock_container[line[0]] = [0,0]
            if line[1] == '365':
                stock_container[line[0]][0] += float(line[2])
            elif line[1] == '730':
                stock_container[line[0]][1] += float(line[2])

    for stock in stock_container:
        init_price, final_price = stock_container[stock][0], stock_container[stock][1]
        if init_price > 0:
            new_container[stock] = (final_price-init_price)/init_price
        else:
            new_container[stock] = 1

    for stock in new_container:
        root = new_container[stock] 
        adjacency_list[stock] = []
        for i in new_container:
            if abs(new_container[i] - root) < threshold:
                if i != stock: # non self-edges
                    adjacency_list[stock].append(i)

def query(stock : str, corr_level : int) -> list:

    ''' OLD BRUTE-FORCE CODE


#    for stock in dict(new_container): # the dict() here prevents: RuntimeError: dictionary changed size during iteration
#        if abs(new_container[stock]) >= t:
#            new_container.pop(stock)

    if corr_level == 1:
        adjacency_list[stock] = qsort(adjacency_list[stock])
        return adjacency_list[stock]
    elif corr_level == 2:
        for x in adjacency_list[stock]:
            adjacency_list[x] = []
        for j in adjacency_list[stock]:
            for i in new_container:
                if abs(new_container[j]-new_container[i]) < t and i != stock and i not in adjacency_list[stock]:
#                    print(str(j)+' '+str(i)+' '+str(abs(new_container[j]-new_container[i])))
                    if i not in adjacency_list[stock]:
                        adjacency_list[j].append(i)
        output = []
        for j in adjacency_list[stock]:
            for k in adjacency_list[j]:
                if k not in output:
                    output.append(k)    
        output = qsort(output)
        return output       
    else:
        return []
    '''

    return qsort(bfs(adjacency_list, stock, corr_level))



# Optional!
def num_connected_components() -> int:
    """ 
        Some stocks can be correlated and create connected componentes / clusters, while others can be alone (not correlated).

        This method should count the number of connected components: 
            A connected component is a set of vertices (stocks) that are linked (correlated) to each other by edges.
         
    Returns:
        int : number of connected components
    """
    # TODO: implement here your approach
    return -1   

def tester(t, s, c):
    prepare("small_dataset2.txt", t)
    return query(s,c)


if __name__ == "__main__":

    print(tester(0.04, "GOOGL", 1))
    print(tester(0.04, "GOOGL", 4))
    print(tester(0.04, "AAPL", 1))
    print(tester(0.04, "AAPL", 2))
    print(tester(0.04, "AAPL", 4))
    print(tester(0.08, "AAPL", 2))

    ncc = num_connected_components()
    # It should return 9 
#    print(ncc)
    mygraph = Graph(adjacency_list)
    edges = mygraph.edges()
    # plot example of graph
    # Driver Code
#    print(bfs(adjacency_list, 'AAPL', 2))   # function calling
#    gplot.plot_graph(edges)
#    bfs([], adjacency_list, 'g')