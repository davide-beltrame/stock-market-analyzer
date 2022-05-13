from math import expm1
from platform import node
import gplot
#from collections import queue
from matplotlib import pyplot as plt
import random 
from email import utils
#from utils import Graph

new_container = {}
adjacency_list = {}

def prepare(filename : str, threshold : float):
    """ The method is responsable to create the needed data structures to 
        answer the queries. 

    Args:
        filename (str): the input file with the dataset
        threshold (float): a special threshold used to compute the correlation between stocks. 
    """
    stock_container = {}
    global new_container

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

    #CORRELATION TEST
    global t
    t = threshold

def qsort(arr):
    if len(arr) <= 1:
        return arr
    else:
        return qsort([x for x in arr[1:] if x < arr[0]]) + [arr[0]] + qsort([x for x in arr[1:] if x >= arr[0]])

def query(stock : str, corr_level : int) -> list:
    """
    Some stocks can be correlated and have a similar behavior.

    This method aims at finding all the correlated stocks respect to the input stock.
    In particular we define the corr_level as follows:
        corr_level = 1 identify all the stocks that are directly correlated to the input stock.
        corr_level = 2 identify all the stocks that are NOT directly correlated to the input stock, but they are correlated through a stock at corr_level = 1. 
        corr_level = 3 identify all the stocks that are NOT directly correlated to the input stock, but they are correlated through a stock at corr_level = 2. 
        ..
        corr_level = i identify all the stocks that are NOT directly correlated to the input stock, but they are correlated through a stock at corr_level = i-1. 
    
    Returns:
        list: a list of correlated stocks at corr_level. The list should be in an alphabetical order. If the stock has not correlated stocks, the output should be an empty list.

    E.g., :
        The execution query(GOOGL, 4) may returns: ['AMZN', 'FISV', 'XEL'] 
        Notice the output is ordered!
    """

#    for stock in dict(new_container): # the dict() here prevents: RuntimeError: dictionary changed size during iteration
#        if abs(new_container[stock]) >= t:
#            new_container.pop(stock)
    global adjacency_list

    centre = new_container[stock] 

    adjacency_list[stock] = []
    for i in new_container:
        if abs(new_container[i] - centre) < t:
            if i != stock: # non self-edges
                adjacency_list[stock].append(i)
    if corr_level == 1:
        adjacency_list[stock] = qsort(adjacency_list[stock])
        return adjacency_list[stock]
    elif corr_level == 2:
        adjacency_list2 = {}
        adjacency_list2[stock] = []
        for j in adjacency_list[stock]:
            for i in new_container:
                if abs(new_container[j]-new_container[i]) < t and i != stock and i not in adjacency_list[stock]:
#                    print(str(j)+' '+str(i)+' '+str(abs(new_container[j]-new_container[i])))
                    if i not in adjacency_list2[stock]:
                        adjacency_list2[stock].append(i)
        adjacency_list2[stock] = qsort(adjacency_list2[stock])
        return adjacency_list2[stock]
    else:
        return []


class Graph():
    """ A data structure for Graph """

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        
    def edges(self):
        all_edges = []
        for key, adj_nodes in self.adjacency_list.items():
            all_edges += [(key, adj_node) for adj_node in adj_nodes]
        return all_edges 


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

# Some code to test your approach (if you need)
if __name__ == "__main__":
    prepare("small_dataset2.txt", 0.04)
    res = query("AAPL", 2) 
    # It should return ['CHTR', 'VRTX']
    print(res)
    print(query("GOOGL", 1))
    ncc = num_connected_components()
    # It should return 9 
#    print(ncc)
    mygraph = Graph(adjacency_list)
    edges = mygraph.edges()
    # plot example of graph
#    gplot.plot_graph(edges)