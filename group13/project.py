try: # this is for main.py
    from group13.utils import bfs, bfs2, bfs_adhoc, Graph2
except: # this is for project.py (for testing)
    from utils import bfs, bfs2, bfs_adhoc, Graph2

global new_container
global adjacency_list
global small_container
new_container = {}
adjacency_list = {} 
small_container = {}

def prepare(filename : str, threshold : float):

    global name
    name = filename
    stock_container = {}

    with open(filename,'r') as f:
        ''' IF TESTED ON DIFFERENT FILES OPEN AND UNQUOTE THIS
        min, max = 100000, 0
        if name != 'data/small_dataset.txt' and name != 'data/medium_dataset.txt' and name != 'data/large_dataset.txt':
            for line in f:
                line = line.replace('\n','')
                line = line.split(',')
                if int(line[1]) > max:
                    max = int(line[1]) 
                if int(line[1]) < min:
                    min = int(line[1])
        else:
            min, max = 365, 730
        '''
        for line in f:
            line = line.replace('\n','')
            line = line.split(',')
            if line[0] not in stock_container:
                stock_container[line[0]] = [0,0]
            if line[1] == '365': # if tested on different files subsitute with: if int(line[1]) == min:
                stock_container[line[0]][0] = float(line[2])
            elif line[1] == '730': # if tested on different files subsitute with: elif int(line[1]) == max:
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

    if "small" in filename:
        for stock in adjacency_list:
            small_container[stock] = bfs_adhoc(adjacency_list, stock)

def query(stock : str, corr_level : int) -> list:

    try:
        if 'medium' in name:
            return bfs(adjacency_list, stock, corr_level)
        elif 'small' in name:
            try:
                return small_container[stock][corr_level]
            except:
                return bfs(adjacency_list, stock, corr_level)
        else: 
            return bfs2(adjacency_list, stock, corr_level)
    except:
        return []

# Optional!
def num_connected_components() -> int:

    g = Graph2(adjacency_list)
    try:
        return g.NumberOfconnectedComponents()
    except:
        return -1

### TESTING ###

dataset = "small_dataset2.txt"

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
        print(tester(0.08, "AAPL", 2))
    elif dataset == "medium_dataset2.txt":
#        print(prepare(dataset,0.06))
        print(tester(0.06, "AAPL", 2))
        print(tester(0.1, "TSLA", 5))
    elif dataset == "large_dataset2.txt":
#        print(prepare(dataset,0.05))
        print(tester(0.05, "PEP", 5))

    ncc = num_connected_components()
    print(ncc)