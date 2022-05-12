from matplotlib import pyplot as plt
import networkx as nx 

from networkx.drawing.nx_pydot import graphviz_layout

class BSTNode:
    def __init__(self, value):
        self.key = value
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.key)
        
def bst_insert(t, value):
    if value <= t.key:
        if t.left:
            bst_insert(t.left, value)
        else:
            t.left = BSTNode(value)
    else:
        if t.right:
            bst_insert(t.right, value)
        else:
            t.right = BSTNode(value)

def bst_search_rec(t, k):
    if t.key == k:
        return t
    if k < t.key:
        return bst_search_rec(t.left, k) if t.left else None
    else:
        return bst_search_rec(t.right, k) if t.right else None


def bst_search(t, k):
    v = t
    while v:
        if v.key == k:
            return v
        elif k < v.key:
            v = v.left
        else:
            v = v.right
    return None

def BST_example(A = [49, 82, 22, 57, 88, 17, 20, 94, 91]):
    """ return an example of BST """
    root = BSTNode(A[0])
    for i in range(1, len(A)):
        bst_insert(root, A[i])
    return root
 

def plot_tree(T, labels, colors=None):
    pos = graphviz_layout(T, prog="dot")
    if colors is not None:
        colors = [colors[t] for t in T.nodes]
    else:
        colors = ["r"] + ["#91cbf2"]* (len(pos)-1)
    nx.draw(T, pos=pos, with_labels=True, node_size=1500, 
    node_color=colors) 
    nx.draw_networkx_edge_labels(T, pos=pos, edge_labels=labels)
    plt.show()

def inorder(t, labels):
    edges = []
    if t.left is not None:
        edges += inorder(t.left, labels)
        edge = (t.key, t.left.key)
        edges += [edge]
        labels[edge] = "left"
    if t.right is not None:
        edges += inorder(t.right, labels)
        edge = (t.key, t.right.key)
        edges += [edge]
        labels[edge] = "right"
    return edges
 
def plot_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos=pos)
    plt.show()

def plot(root_node, colors=None):
    labels = {}
    tree_edegs = inorder(root_node, labels)
    T = nx.DiGraph()
    T.add_node(root_node.key)
    T.add_edges_from(tree_edegs)
    plot_tree(T, labels, colors)
    
