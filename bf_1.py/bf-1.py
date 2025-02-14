def bestFit(weight, n, c):
    """
    Implements the Best Fit bin packing algorithm.

    Args:
        weight: A list of integers representing the weights of the items.
        n: The number of items.
        c: The capacity of each bin.

    Returns:
        A tuple containing:
            - The number of bins used.
            - A list representing the number of items in each bin.
    """
    res = 0
    bin_rem = [0] * n
    bin_items = [[] for _ in range(n)]  # Initialize a list to store items in each bin

    for i in range(n):
        min = c + 1
        bi = 0
        for j in range(res):
            if bin_rem[j] >= weight[i] and bin_rem[j] - weight[i] < min:
                bi = j
                min = bin_rem[j] - weight[i]
        if min == c + 1:
            bin_rem[res] = c - weight[i]
            bin_items[res].append(weight[i])  # Add item to the new bin
            res += 1
        else:
            bin_rem[bi] -= weight[i]
            bin_items[bi].append(weight[i])  # Add item to the existing bin

    return res, bin_items



# Example usage
weight = [2, 5, 4, 7, 1, 3, 8]
c = 10
num_bins, bin_items = bestFit(weight, len(weight), c)

print("Number of bins required in Best Fit:", num_bins)
print("Items in each bin:", bin_items)

def next_fit(item_weights, bin_capacity):
  """
  Calculates the number of bins needed to pack items and returns the bin contents.
  Next Fit

  Args:
    item_weights: A list of integers representing the weights of the items.
    bin_capacity: The maximum capacity of each bin.

  Returns:
    A tuple containing:
      - The number of bins used.
      - A list of lists, where each sublist represents the items in a bin.
  """
  bins = []
  current_bin = []
  current_bin_weight = 0

  for item_weight in item_weights:
    if item_weight > bin_capacity:
      # If the item doesn't fit in any bin, create a new bin
      bins.append(current_bin)
      current_bin = [item_weight]
      current_bin_weight = item_weight
    else:
      # If the item fits in the current bin, add it
      if current_bin_weight + item_weight <= bin_capacity:
        current_bin.append(item_weight)
        current_bin_weight += item_weight
      else:
        # If the item doesn't fit in the current bin, create a new bin
        bins.append(current_bin)
        current_bin = [item_weight]
        current_bin_weight = item_weight

  # Add the last bin if it's not empty
  if current_bin:
    bins.append(current_bin)

  return len(bins), bins

# Example usage
item_weights = [2, 5, 4, 7, 1, 3, 8]
bin_capacity = 10

num_bins, bin_contents = next_fit(item_weights, bin_capacity)

print("Number of bins required:", num_bins)
print("Next Fit Bin contents:", bin_contents)

def first_fit(items, bin_capacity):
  """
  Implémente l'algorithme First Fit pour le problème du bin packing.

  Args:
    items: Une liste d'entiers représentant les tailles des objets.
    bin_capacity: La capacité maximale de chaque bin.

  Returns:
    Une liste de listes, où chaque sous-liste représente les éléments d'un bin.
  """

  bins = []
  for item in items:
    found_bin = False
    for bin in bins:
      if sum(bin) + item <= bin_capacity:
        bin.append(item)
        found_bin = True
        break
    if not found_bin:
      bins.append([item])

  return bins

# Exemple d'utilisation
items = [2, 5, 4, 7, 1, 3, 8]
bin_capacity = 10

result = first_fit(items, bin_capacity)

print("Contenu des bins:")
for i, bin in enumerate(result):
  print(f"Bin {i+1}: {bin}")