from bosque_py import Tree
from scipy.spatial import cKDTree as scipyTree
import numpy as np
from time import perf_counter as time

DATA = 100_000
QUERY = 1_000_000
ITERS = 100

# Bosque only works for d=3 right now
DIM = 3
K = 2
K_SPARSE = [1, 2, 4]

data = np.random.uniform(size=(DATA, DIM))
query = np.random.uniform(size=(QUERY, DIM))
idxs = np.arange(DATA)

print("-------------------------- bosque results -------------------------")

start = time()
for _ in range(ITERS):
    tree = Tree(data)
print(f"bosque finished build in {int(1000*(time()-start) / ITERS)} millis")

start = time()
for _ in range(ITERS):
    r, ids = tree.query(query, K)
print(f"bosque finished query in {int(1000*(time()-start) / ITERS)} millis")

start = time()
for _ in range(ITERS):
    r, ids = tree.query(query, K, [0, 1])
print(f"bosque periodic query in {int(1000*(time()-start) / ITERS)} millis")

start = time()
for _ in range(ITERS):
    r, ids = tree.query(query, K_SPARSE)
print(f"bosque k-sparse query in {int(1000*(time()-start) / ITERS)} millis")

print("-------------------------- scipy results --------------------------")
start = time()
for _ in range(ITERS):
    stree = scipyTree(data)
print(f"scipy finished build in {int(1000*(time()-start) / ITERS)} millis")

start = time()
for _ in range(ITERS):
    sr, sids = stree.query(query, K if K > 1 else [K], workers=-1)
print(f"scipy finished query in {int(1000*(time()-start) / ITERS)} millis")

stree_periodic = scipyTree(data, boxsize = [1.0, 1.0, 1.0])
start = time()
for _ in range(ITERS):
    sr, sids = stree_periodic.query(query, K if K > 1 else [K], workers=-1)
print(f"scipy periodic query in {int(1000*(time()-start) / ITERS)} millis")

start = time()
for _ in range(ITERS):
    sr, sids = stree.query(query, K_SPARSE, workers=-1)
print(f"scipy k-sparse query in {int(1000*(time()-start) / ITERS)} millis")

print("-------------------------------------------------------------------")


print(f"Average distance for {DATA} points in unit cube is ≈{DATA**(-1/3)}")
for (i, k) in enumerate(K_SPARSE):
    # Sparse query is the last one to execute, enumerate gets right indices
    print(f"measured {k}NN mean is = {r[:,i].mean()} vs {sr[:,i].mean()}")