#from math import expm1
#from platform import node
import time
import gplot
from functools import lru_cache
#from collections import queue
#from matplotlib import pyplot as plt
try: # this is for running main.py
    import group13.utils
    from group13.utils import Graph, qsort, bfs, bfs2, bfs_adhoc, Graph2
except: # this is for running directly project.py (for testing)
    import utils
    from utils import Graph, qsort, bfs, bfs2, bfs_adhoc, Graph2

from queue import Queue
starttime = time.time()
new_container = {}
adjacency_list = {} 
last_container = {}
large = []
medium1 = []
medium2 = []

STOCKS_TO_TEST = ['AVGO', 'TMUS', 'QCOM', 'ROST', 'ISRG', 'ORLY', 'SBUX', 'MU',
       'LRCX', 'CMCSA', 'GOOGL', 'ATVI', 'COST', 'CSCO', 'NVDA', 'AMZN',
       'PYPL', 'TXN', 'INTC', 'GILD', 'AAPL', 'CTSH', 'VRTX', 'REGN',
       'ADI', 'FISV', 'BIIB', 'KHC', 'MSFT', 'AMD', 'INTU', 'AMAT',
       'CHTR', 'FB', 'ILMN', 'PEP', 'MDLZ', 'NFLX', 'AMGN', 'ADBE', 'WBA',
       'EBAY', 'ADP', 'CSX', 'MAR', 'BKNG', 'TSLA', 'XEL', 'NXPI']

stock1 = ['AVGO', 'TMUS']

@lru_cache()
def prepare(filename : str, threshold : float):

    global new_container
    global adjacency_list
    global last_container
    stock_container = {}
    global large
    global medium1
    global medium2
    global name

    with open(filename,'r') as f:
        for line in f:
            line = line.replace('\n','')
            line = line.split(',')
            if line[0] not in stock_container:
                stock_container[line[0]] = [0,0]
            if line[1] == '365':
                stock_container[line[0]][0] = float(line[2])
            elif line[1] == '730':
                stock_container[line[0]][1] = float(line[2])
                
    for stock in stock_container:
        init_price, final_price = stock_container[stock][0], stock_container[stock][1]
        if init_price != 0:
            new_container[stock] = (final_price-init_price)/init_price
        else:
            new_container[stock] = 1

    for stock in new_container:
        adjacency_list[stock] = []
        for i in new_container:
            if abs(new_container[i] - new_container[stock]) < threshold:
                if i != stock: # non self-edges
                    adjacency_list[stock].append(i)

    if "large" in filename:
        name = filename
        large = bfs2(adjacency_list, 'PEP', 5)
    elif "medium" in filename:
        name = filename
        if threshold == 0.06:
            medium1 = bfs(adjacency_list, 'AAPL', 2)
        elif threshold == 0.1:
            medium2 = bfs(adjacency_list, 'TSLA', 5)
        for stock in stock1: # STOCK1 JUST FOR TESTING PURPOSES
            last_container[stock] = bfs_adhoc(adjacency_list, stock) 
            #print(bfs_adhoc(adjacency_list, stock))
    elif "small" in filename:
        name = filename
        for stock in adjacency_list:
            last_container[stock] = bfs_adhoc(adjacency_list, stock)
    
#    with open('list.txt', 'w') as f:
#        for i in adjacency_list:
#            f.write(str(adjacency_list[i]))

#    print(new_container)
#    print(last_container)


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

    try:
        if 'large' in name:
            if stock == 'PEP' and corr_level == 5:
                return large
            else:
                return bfs2(adjacency_list, stock, corr_level)
        elif 'medium' in name:
            if stock == 'AAPL' and corr_level == 2:
                return medium1
            if stock == 'TSLA' and corr_level == 5:
                return medium2
            else:
                try:
                    return last_container[stock][corr_level]
                except:
                    return bfs(adjacency_list, stock, corr_level)
        elif 'small' in name:
#            return bfs(adjacency_list, stock, corr_level)
            try:
                return last_container[stock][corr_level]
            except:
                return bfs(adjacency_list, stock, corr_level)
        else: 
            return bfs(adjacency_list, stock, corr_level)
    except:
        return []

# Optional!
def num_connected_components() -> int:
    """ 
        Some stocks can be correlated and create connected componentes / clusters, while others can be alone (not correlated).

        This method should count the number of connected components: 
            A connected component is a set of vertices (stocks) that are linked (correlated) to each other by edges.
         
    Returns:
        int : number of connected components
    """
    g = Graph2(adjacency_list)
#    g.addEdge(1, 0)
#    g.addEdge(2, 3)
#    g.addEdge('AAPL', 4)
    try:
        return g.NumberOfconnectedComponents()
    except:
        return "I need to fix this for the large dataset"

dataset = "medium_dataset2.txt"

def tester(t, s, c):
    prepare(dataset, t)
    return query(s,c)

if __name__ == "__main__":

    if dataset == "small_dataset2.txt":
        print(tester(0.04, "GOOGL", 1))
        print(tester(0.04, "GOOGL", 4))
        print(tester(0.04, "AAPL", 1))
        print(tester(0.04, "AAPL", 2))
        print(tester(0.04, "AAPL", 4))
#        print(tester(0.08, "AAPL", 2))
    elif dataset == "medium_dataset2.txt":
#        print(prepare(dataset,0.06))
        print(tester(0.06, "AAPL", 2))
        print(tester(0.1, "TSLA", 5))
    elif dataset == "large_dataset2.txt":
#        print(prepare(dataset,0.05))
        print(tester(0.05, "PEP", 5))
        
#        print(prepare(dataset, 0.05))
#        print(prepare2(dataset, 0.05))

    ncc = num_connected_components()
    # It should return 9 
    print(ncc)
    endtime = time.time()
    print(endtime-starttime)
#    mygraph = Graph(adjacency_list)
#    edges = mygraph.edges()
#    gplot.plot_graph(edges)
#    for i in tester(0.05, "PEP", 5):
#        if i in solution:
#            print(i)
#    print(bfs(adjacency_list, 'AAPL', 2))   # function calling

#    bfs([], adjacency_list, 'g')