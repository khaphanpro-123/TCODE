# Inversion Problems (BIT / Mo)

This module `inversions_problems.py` contains solutions for the following tasks:

1. Check whether an array is "nearly sorted" (number of inversions ≤ k)
2. Number of swaps bubble sort needs (equal to inversion count)
3. For each position i, number of inversions after removing A[i]
4. Queue overtakes: seconds until stable when taller people overtake front
5. Count inversions in subarray queries using Mo's algorithm + Fenwick
6. Minimal adjacent swaps to transform permutation A into B (inversion count)

Quick run:

```bash
python -m inversions_problems
```

Notes:
- The implementations use a Fenwick tree (BIT) and coordinate compression.
- For query problem (5) we implemented Mo's algorithm with a Fenwick for updates in O((n+q) * sqrt(n) * log n) roughly.

To push these files to GitHub, add a remote and push:

```bash
git remote add origin <URL>
git branch -M main
git push -u origin main
```
