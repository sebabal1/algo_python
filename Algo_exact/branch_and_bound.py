from collections import defaultdict

def branch_and_bound(items, bin_capacity):
    """
    Implémentation du branch-and-bound pour le problème du bin packing, avec affichage des bacs

    Args:
        items: Liste des tailles des objets
        bin_capacity: Capacité maximale d'un bac

    Returns:
        Nombre minimal de bacs nécessaires et le contenu de chaque bac
    """

    class Node:
        def __init__(self, items_remaining, level, bins):
            self.items_remaining = items_remaining
            self.level = level
            self.bins = bins  # Liste de listes, chaque sous-liste représente un bac
            self.bound = sum(items_remaining) // bin_capacity 

        def is_leaf(self):
            return len(self.items_remaining) == 0

    def branch(node):
        # Créer deux nœuds enfants : un où l'objet est placé dans le dernier bac utilisé,
        # et un autre où l'objet est placé dans un nouveau bac
        for i in range(node.level + 1):
            new_bins = node.bins.copy()
            if sum(new_bins[i]) + node.items_remaining[0] <= bin_capacity:
                new_bins[i].append(node.items_remaining[0])
                yield Node(node.items_remaining[1:], node.level, new_bins)
        new_bins = node.bins.copy()
        new_bins.append([node.items_remaining[0]])
        yield Node(node.items_remaining[1:], node.level + 1, new_bins)

    # Initialisation
    best_solution = len(items)
    best_bins = None
    root = Node(items, 0, [[]])
    stack = [root]

    while stack:
        node = stack.pop()
        if node.is_leaf():
            if node.level < best_solution:
                best_solution = node.level
                best_bins = node.bins
        else:
            for child in branch(node):
                if child.bound <= best_solution:
                    stack.append(child)

    return best_solution, best_bins

# Exemple d'utilisation
items = [5, 3, 4, 2, 8, 1, 6]
bin_capacity = 10
result, bins = branch_and_bound(items, bin_capacity)
print("Nombre minimal de bacs:", result)
for i, bin_contents in enumerate(bins):
    print(f"Bac {i+1}: {bin_contents}")