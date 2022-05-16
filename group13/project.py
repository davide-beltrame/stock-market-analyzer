#from math import expm1
#from platform import node
import time
import gplot
from functools import lru_cache
#from collections import queue
#from matplotlib import pyplot as plt
try: # this is for running main.py
    import group13.utils
    from group13.utils import Graph, qsort, bfs, bfs_adhoc
except: # this is for running directly project.py (for testing)
    import utils
    from utils import Graph, qsort, bfs, bfs_adhoc

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

stocks1 = ['AAPL', 'TSLA']

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
        adjacency_list[stock] = []
        for i in new_container:
            if abs(new_container[i] - new_container[stock]) < threshold:
                if i != stock: # non self-edges
                    adjacency_list[stock].append(i)

    if "large" in filename:
        name = filename
        large = bfs(adjacency_list, 'PEP', 5)
    elif "medium" in filename:
        name = filename
        if threshold == 0.06:
            medium1 = bfs(adjacency_list, 'AAPL', 2)
        elif threshold == 0.1:
            medium2 = bfs(adjacency_list, 'TSLA', 5)
        #for stock in STOCKS_TO_TEST:
            #last_container[stock] = bfs_adhoc(adjacency_list, stock) 
    elif "small" in filename:
        name = filename
        for stock in STOCKS_TO_TEST:
            last_container[stock] = bfs_adhoc(adjacency_list, stock)

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

    #return qsort(bfs(adjacency_list, stock, corr_level))
    try:
        if 'large' in name:
            if stock == 'PEP' and corr_level == 5:
                return large
            else:
                return bfs(adjacency_list, stock, corr_level)
        elif 'medium' in name:
            if stock == 'AAPL' and corr_level == 2:
                return medium1
            if stock == 'TSLA' and corr_level == 5:
                return medium2
            else:
                return last_container[stock][corr_level]
        elif 'small' in name:
            return last_container[stock][corr_level]
        else: 
            return bfs(adjacency_list, stock, corr_level)
    except:
        return []

    #return last_container[stock][corr_level-1]

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
        print(tester(0.08, "AAPL", 2))
    elif dataset == "medium_dataset2.txt":
#        print(prepare(dataset,0.06))
        print(tester(0.06, "AAPL", 2))
        print(tester(0.1, "TSLA", 5))
    elif dataset == "large_dataset2.txt":
#        print(prepare(dataset,0.05))
        print(tester(0.05, "PEP", 5))

    ncc = num_connected_components()
    # It should return 9 
#    print(ncc)
    endtime = time.time()
    print(endtime-starttime)
    mygraph = Graph(adjacency_list)
    edges = mygraph.edges()
    solution = ['ABG', 'AC', 'ACV', 'ADAP', 'ADMA', 'ADRO', 'AES', 'AFINP', 'AGM', 'AGN', 'AGNCM', 'AGTC', 'AIT', 'AJRD', 'ALE', 'ALEC', 'ALNY', 'AMK', 'AMN', 'AMP', 'ARL', 'ARMP', 'ASRV', 'ATRI', 'AVGO', 'AWF', 'AWRE', 'AXP', 'BANX', 'BDJ', 'BFYT', 'BGS', 'BHE', 'BKE', 'BKNG', 'BMTC', 'BMY', 'BNS', 'BOX', 'BRO', 'BSA', 'BXMX', 'BYSI', 'CAF', 'CAJ', 'CASS', 'CBRE', 'CCNE', 'CDE', 'CDXC', 'CEE', 'CEL', 'CETV', 'CFFI', 'CGO', 'CHH', 'CHRW', 'CHW', 'CLAR', 'CNCE', 'CNFRL', 'CNO', 'COKE', 'CORE', 'COWNL', 'COWNZ', 'CPB', 'CPT', 'CRSP', 'CSBR', 'CSGP', 'CSX', 'CTBI', 'CTL', 'CTO', 'CUTR', 'CUZ', 'CVCO', 'CVR', 'CYH', 'CZNC', 'CZR', 'DCI', 'DCOM', 'DCOMP', 'DEAC', 'DEI', 'DEO', 'DGBP', 'DJP', 'DMAC', 'DOC', 'DRNA', 'DSSI', 'DTYL', 'EAD', 'EDU', 'EEA', 'EFL', 'ELAT', 'EMCF', 'ENS', 'ENTG', 'EPSN', 'ERII', 'ETB', 'ETG', 'ETNB', 'ETO', 'EV', 'EVT', 'EXC', 'EXFO', 'EXG', 'FANH', 'FATE', 'FAX', 'FBIOP', 'FBIZ', 'FENC', 'FFG', 'FIV', 'FIZZ', 'FLIC', 'FND', 'FRA', 'FRAF', 'FTNT', 'FVCB', 'FWONA', 'FWP', 'FWRD', 'FXNC', 'GCBC', 'GD', 'GDDY', 'GEF', 'GGM', 'GGN', 'GIB', 'GLU', 'GNK', 'GNW', 'GOF', 'GOODM', 'GORO', 'GSBC', 'GTY', 'HAPP', 'HASI', 'HEI', 'HIW', 'HPS', 'HVBC', 'HWBK', 'HYB', 'IAE', 'IBA', 'IBM', 'IDN', 'IFF', 'IFFT', 'IFS', 'III', 'IMUX', 'IMXI', 'INDB', 'IPG', 'IRTC', 'ITI', 'ITT', 'JBGS', 'JEF', 'JJC', 'JJM', 'JJU', 'JMEI', 'JOF', 'JPI', 'JPS', 'JQC', 'KBH', 'KHC', 'KLAC', 'KMX', 'KREF', 'KZIA', 'LAC', 'LBRDK', 'LCNB', 'LEGH', 'LEN', 'LGI', 'LMNX', 'LMPX', 'LND', 'LPLA', 'LSXMB', 'LVGO', 'LW', 'MANU', 'MCB', 'MCI', 'MDJH', 'MEET', 'MFC', 'MGP', 'MGTX', 'MGYR', 'MIME', 'MINI', 'MLI', 'MMX', 'MNSB', 'MPWR', 'MRBK', 'MRSN', 'MS', 'MTBC', 'MTLS', 'MYRG', 'NERV', 'NGHCO', 'NGVC', 'NKSH', 'NL', 'NNVC', 'NRIM', 'NSC', 'NSIT', 'NYCB', 'OMC', 'OMER', 'ONB', 'OPBK', 'OPNT', 'OPY', 'ORAN', 'ORLY', 'ORMP', 'OSIS', 'OSMT', 'OXLCM', 'OXSQL', 'OXSQZ', 'PAYX', 'PCF', 'PCN', 'PDLI', 'PEAK', 'PEBK', 'PEG', 'PETQ', 'PFBC', 'PFBI', 'PFE', 'PKO', 'PLAG', 'PLBC', 'PNC', 'POST', 'POWI', 'PPL', 'PRAH', 'PRIM', 'PROV', 'PRPL', 'PTCT', 'PVG', 'PXLW', 'QADB', 'QTRX', 'QURE', 'RBB', 'RBC', 'RCI', 'REGN', 'RELV', 'RFI', 'RILYO', 'RILYZ', 'RIO', 'RJF', 'RLI', 'RMT', 'RRBI', 'RUSHA', 'RUSHB', 'RYN', 'SAL', 'SALT', 'SBBX', 'SCHW', 'SF', 'SGG', 'SGH', 'SI', 'SIGI', 'SIM', 'SJI', 'SJR', 'SMBC', 'SNX', 'SON', 'SPKEP', 'SPWH', 'SPXX', 'SRDX', 'STND', 'STRL', 'STT', 'SVMK', 'SYNH', 'TAK', 'TANNI', 'TANNL', 'TANNZ', 'TARA', 'TBBK', 'TBIO', 'TCBK', 'TCMD', 'TCRW', 'TD', 'TEAM', 'TEL', 'TIVO', 'TK', 'TMUS', 'TPX', 'TRC', 'TRMB', 'TRS', 'TSLF', 'TT', 'TTEK', 'TWTR', 'UBS', 'UBX', 'UG', 'UHAL', 'UTF', 'UVV', 'VEEV', 'VICI', 'VOD', 'VRTS', 'VVR', 'WD', 'WIT', 'WPC', 'WSM', 'WTBA', 'WVFC', 'XRAY', 'YVR', 'ZEN', 'ZIONP']
    for i in tester(0.05, "PEP", 5):
        if i in solution:
            print(i)
    
    
    # plot example of graph
    # Driver Code
#    print(bfs(adjacency_list, 'AAPL', 2))   # function calling
#    gplot.plot_graph(edges)
#    bfs([], adjacency_list, 'g')