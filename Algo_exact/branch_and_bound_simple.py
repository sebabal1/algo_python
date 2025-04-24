import time

class BinPackingBnB:
    def __init__(self, items, bin_capacity):
        self.items = items
        self.bin_capacity = bin_capacity
        self.n = len(items)
        self.best_num_bins = float('inf')
        self.best_assignment = [[] for _ in range(self.n)]

    def solve(self):
        start_time = time.time()
        self._branch_and_bound(0, [], 0)
        end_time = time.time()
        execution_time = end_time - start_time
        return self.best_num_bins, self.best_assignment[:self.best_num_bins], execution_time

    def _branch_and_bound(self, item_index, bins, num_bins):
        # Borne inférieure (nombre minimum de bacs nécessaires)
        lower_bound = num_bins + (sum(self.items[item_index:]) + self.bin_capacity - 1) // self.bin_capacity
        print(f'Borne : {lower_bound}')
        print(f'Capacité bin : {self.bin_capacity}')
        print(f'Best num bins : {self.best_num_bins}')
        if lower_bound >= self.best_num_bins:
            return

        print(f'Item : {item_index}')
        print(f'Valeur : {self.n}')
        print(f'Num bins : {num_bins}')
        if item_index == self.n:
            if num_bins < self.best_num_bins:
                self.best_num_bins = num_bins
                self.best_assignment = [bin[:] for bin in bins]
            return

        print(f'Item en cours : {self.items[item_index]}')
        # Essayer de placer l'objet courant dans un bac existant
        for i in range(num_bins):
            if sum(bins[i]) + self.items[item_index] <= self.bin_capacity:
                bins[i].append(self.items[item_index])
                self._branch_and_bound(item_index + 1, bins, num_bins)
                bins[i].pop()  # Backtrack

        # Essayer de placer l'objet courant dans un nouveau bac
        bins.append([self.items[item_index]])
        print(f'Bin : {bins}')
        self._branch_and_bound(item_index + 1, bins, num_bins + 1)
        bins.pop()  # Backtrack

# Exemple d'utilisation
items = [2, 5, 1, 7, 3, 8]
bin_capacity = 10
solver = BinPackingBnB(items, bin_capacity)
num_bins, assignment, execution_time = solver.solve()

print(f"Nombre minimum de bacs nécessaires : {num_bins}")
print("Répartition des objets dans les bacs :")
for i, bin_items in enumerate(assignment):
    print(f"Bac {i + 1}: {bin_items}")
print(f"Temps d'exécution : {execution_time:.4f} secondes")