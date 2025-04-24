from pulp import *
import math

def solve_bin_packing_pulp(items, bin_capacity):
    """
    Résout le problème de Bin Packing en utilisant PuLP.

    Args:
        items (list): Une liste des poids des objets.
        bin_capacity (int): La capacité de chaque boîte.

    Returns:
        tuple: Un tuple contenant :
            - optimal_bins (dict): Un dictionnaire représentant le contenu de chaque boîte utilisée.
            - min_bins (int): Le nombre minimum de boîtes utilisées.
    """
    num_items = len(items)
    max_bins = num_items  # Au pire, chaque objet va dans sa propre boîte

    # Indices des objets et des boîtes
    item_indices = range(num_items)
    bin_indices = range(max_bins)

    # Créer le problème de programmation linéaire en nombres entiers
    prob = LpProblem("Bin Packing Problem", LpMinimize)

    # Variables de décision
    # y[j] = 1 si la boîte j est utilisée, 0 sinon
    y = LpVariable.dicts("UseBin", bin_indices, 0, 1, LpInteger)

    # x[i][j] = 1 si l'objet i est placé dans la boîte j, 0 sinon
    x = LpVariable.dicts("ItemInBin", (item_indices, bin_indices), 0, 1, LpInteger)

    # Fonction objectif : minimiser le nombre de boîtes utilisées
    prob += lpSum(y[j] for j in bin_indices), "Minimize Number of Bins"

    # Contraintes
    # 1. Chaque objet doit être placé dans exactement une boîte
    for i in item_indices:
        prob += lpSum(x[i][j] for j in bin_indices) == 1, f"Item_{i}_Placed"

    # 2. La capacité de chaque boîte ne doit pas être dépassée
    for j in bin_indices:
        prob += lpSum(items[i] * x[i][j] for i in item_indices) <= bin_capacity * y[j], f"Bin_{j}_Capacity"

    # Résoudre le problème en utilisant le solveur par défaut de PuLP (qui peut être CBC)
    prob.solve()

    # Vérifier le statut de la solution
    if LpStatus[prob.status] == "Optimal":
        min_bins = int(value(prob.objective))
        optimal_bins = {j: [] for j in bin_indices if value(y[j]) == 1}
        for i in item_indices:
            for j in bin_indices:
                if value(x[i][j]) == 1 and j in optimal_bins:
                    optimal_bins[j].append(items[i])
        return optimal_bins, min_bins
    else:
        return None, None

if __name__ == '__main__':
    items = [2, 5, 1, 7, 3, 8]
    bin_capacity = 10
    optimal_bins, min_bins = solve_bin_packing_pulp(items, bin_capacity)

    if optimal_bins:
        print("Solution optimale trouvée :")
        print(f"Nombre minimum de boîtes utilisées : {min_bins}")
        for bin_num, contents in optimal_bins.items():
            print(f"Boîte {bin_num + 1} : {contents}")
    else:
        print("Aucune solution optimale trouvée.")