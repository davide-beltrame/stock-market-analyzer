from email import utils
from utils import Graph

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

    return new_container

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

    if corr_level == 2:
        adjacency_list2 = {}
        adjacency_list2[stock] = []
        for j in adjacency_list[stock]:
            for i in new_container:
                if abs(new_container[j]-new_container[i]) < t and i != stock and i not in adjacency_list[stock]:
                    print(str(j)+' '+str(i)+' '+str(abs(new_container[j]-new_container[i])))
                    if i not in adjacency_list2[stock]:
                        adjacency_list2[stock].append(i)

    print(adjacency_list)
    return adjacency_list2

#    return []

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
    print(prepare("small_dataset2.txt", 0.05))
    res = query("AAPL", corr_level = 2) 
    # It should return ['CHTR', 'VRTX']
    print(res)
    ncc = num_connected_components()
    # It should return 9 
#    print(ncc)
    
'''
pip install matplotlib
pip install networkx
pip install pydot
pip install graphviz / conda install graphviz
'''

# DATA STRUCTURE

# sufficient
'''
{'AAPL': [(371.0, 200.0), (369.0, 197.0), (370.0, 200.0), 
(365.0, 191.0), (366.0, 194.0), (367.0, 195.0), (368.0, 196.0)], 
'TSLA': [(369.0, 275.0), (370.0, 273.0), (371.0, 273.0), 
(365.0, 289.0), (366.0, 286.0), (367.0, 292.0), (368.0, 268.0)]}
'''

# complete
'''
{'AAPL': [(730.0, 200.0, 0.0), (369.0, 197.0, 18526600.0), 
(370.0, 200.0, 0.0), (365.0, 191.0, 27862000.0), 
(366.0, 194.0, 22765700.0), (367.0, 195.0, 23271800.0), (368.0, 196.0, 19114300.0)], 
'TSLA': [(369.0, 275.0, 13038300.0), (370.0, 273.0, 0.0), 
(730.0, 273.0, 0.0), (365.0, 289.0, 8110400.0), 
(366.0, 286.0, 5478900.0), (367.0, 292.0, 7929900.0), (368.0, 268.0, 23720700.0)]}
'''