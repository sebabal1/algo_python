import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, items_remaining, level, bins, bound, id):
        self.items_remaining = items_remaining
        self.level = level
        self.bins = bins
        self.bound = bound
        self.id = id

    def is_leaf(self):
        return len(self.items_remaining) == 0

def branch(node, bin_capacity):
    children = []
    for i in range(len(node.bins)):  
        if sum(node.bins[i]) + node.items_remaining[0] <= bin_capacity: 
            new_bins = node.bins.copy()
            new_bins[i].append(node.items_remaining[0])
            children.append(Node(node.items_remaining[1:], node.level, new_bins, 
                                 calculate_bound(new_bins, node.items_remaining[1:], bin_capacity), 
                                 len(children))) 
    if not children:
        new_bins = node.bins.copy()
        new_bins.append([node.items_remaining[0]])
        children.append(Node(node.items_remaining[1:], node.level + 1, new_bins, 
                             calculate_bound(new_bins, node.items_remaining[1:], bin_capacity), 
                             len(children)))
    return children

def calculate_bound(bins, remaining_items, bin_capacity):
    # Calcul d'une borne inférieure simple (somme des objets restants divisée par la capacité du bac)
    return sum(remaining_items) // bin_capacity

def branch_and_bound(items, bin_capacity):
    """
    Implémentation du branch-and-bound pour le problème du bin packing, 
    avec création de l'arbre de décision.

    Args:
        items: Liste des tailles des objets
        bin_capacity: Capacité maximale d'un bac

    Returns:
        Nombre minimal de bacs nécessaires, le contenu de chaque bac, 
        le nœud racine de l'arbre de décision
    """
    best_solution = len(items)
    best_bins = None
    root = Node(items, 0, [[]], sum(items) // bin_capacity, 0) 
    stack = [root]
    
    while stack:
        node = stack.pop()
        if node.is_leaf():
            if node.level < best_solution:
                best_solution = node.level
                best_bins = node.bins
        else:
            for child in branch(node, bin_capacity):
                if child.bound <= best_solution:
                    stack.append(child)

    return best_solution, best_bins, root

def create_branch_and_bound_graph(root_node, bin_capacity):
    """
    Crée un graphe NetworkX représentant l'arbre de décision.

    Args:
        root_node: Le nœud racine de l'arbre.
        bin_capacity: Capacité maximale d'un bac

    Returns:
        Un objet NetworkX Graph.
    """

    G = nx.DiGraph()

    def add_node_and_edges(node, parent=None):
        node_label = f"Niveau: {node.level}\nBacs: {node.bins}\nRestants: {node.items_remaining}\nBorne: {node.bound}"
        G.add_node(node.id, label=node_label)
        if parent is not None:
            G.add_edge(parent, node.id)
        for child in branch(node, bin_capacity):  
            add_node_and_edges(child, node.id)

    add_node_and_edges(root_node)
    return G

# Exemple d'utilisation
items = [5, 3, 4, 2, 8, 1, 6]
bin_capacity = 10
best_solution, best_bins, root_node = branch_and_bound(items, bin_capacity)

# Créer le graphe de l'arbre de décision
tree_graph = create_branch_and_bound_graph(root_node, bin_capacity)  # Passer bin_capacity à la fonction

# Dessiner le graphe
pos = nx.spring_layout(tree_graph)
nx.draw(tree_graph, pos, with_labels=True, font_size=8) 
plt.show()