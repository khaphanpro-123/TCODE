"""Inversion-related problems using Fenwick Tree (BIT) and Mo's algorithm.

Problems implemented:
1) Check nearly sorted: inversions <= k
2) Bubble swaps needed = inversion count
3) Inversions after removing each element
4) Queue overtakes: seconds until stable (parallel adjacent swaps when right>left)
5) Count inversions in subarray queries using Mo + BIT
6) Minimal adjacent swaps to transform permutation A into B

Simple CLI and tests at bottom.
"""
from __future__ import annotations

from typing import List, Tuple
from bisect import bisect_left
from math import sqrt


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx: int, val: int = 1) -> None:
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx: int) -> int:
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx -= idx & -idx
        return s

    def range_sum(self, l: int, r: int) -> int:
        if r < l:
            return 0
        return self.sum(r) - self.sum(l - 1)


def compress(arr: List[int]) -> Tuple[List[int], dict]:
    vals = sorted(set(arr))
    comp = {v: i + 1 for i, v in enumerate(vals)}
    return [comp[x] for x in arr], comp


def inversion_count(arr: List[int]) -> int:
    if not arr:
        return 0
    comp_arr, _ = compress(arr)
    nval = max(comp_arr)
    bit = Fenwick(nval)
    inv = 0
    # scan from right, count how many smaller seen
    for x in reversed(comp_arr):
        inv += bit.sum(x - 1)
        bit.add(x, 1)
    return inv


# Problem 1
def is_nearly_sorted(arr: List[int], k: int) -> bool:
    return inversion_count(arr) <= k


# Problem 2
def bubble_swaps_needed(arr: List[int]) -> int:
    return inversion_count(arr)


# Problem 3
def inversions_after_removal(arr: List[int]) -> List[int]:
    n = len(arr)
    if n == 0:
        return []
    comp_arr, _ = compress(arr)
    nval = max(comp_arr)
    bit = Fenwick(nval)
    leftGreater = [0] * n
    # leftGreater[i] = count of elements to left greater than arr[i]
    for i in range(n):
        x = comp_arr[i]
        leftGreater[i] = i - bit.sum(x)  # number seen - <= x
        bit.add(x, 1)
    # reset BIT
    bit = Fenwick(nval)
    rightSmaller = [0] * n
    # rightSmaller[i] = count of elements to right smaller than arr[i]
    for i in range(n - 1, -1, -1):
        x = comp_arr[i]
        rightSmaller[i] = bit.sum(x - 1)
        bit.add(x, 1)
    total_inv = sum(leftGreater)
    res = [total_inv - (leftGreater[i] + rightSmaller[i]) for i in range(n)]
    return res


# Problem 4: Queue overtakes (parallel adjacent swaps when right>left)
# We simulate rounds using a set of candidate indices where arr[i] < arr[i+1].
# Each round we perform non-overlapping swaps from left to right.

def queue_overtake_time(arr: List[int]) -> int:
    n = len(arr)
    if n <= 1:
        return 0
    a = arr[:]  # copy
    # set of indices i where a[i] < a[i+1]
    candidates = [i for i in range(n - 1) if a[i] < a[i + 1]]
    time = 0
    while candidates:
        time += 1
        to_swap = []
        skip = -1
        for i in candidates:
            if i <= skip:
                continue
            # verify condition still holds (it should)
            if a[i] < a[i + 1]:
                to_swap.append(i)
                skip = i + 1
        if not to_swap:
            break
        # perform swaps
        for i in to_swap:
            a[i], a[i + 1] = a[i + 1], a[i]
        # recompute candidates near swaps
        new_cand = set()
        for i in to_swap:
            for j in (i - 1, i, i + 1):
                if 0 <= j < n - 1 and a[j] < a[j + 1]:
                    new_cand.add(j)
        # Also keep candidates that were not affected
        for i in candidates:
            if i not in new_cand and all(not (i >= s and i <= s + 1) for s in to_swap):
                # unchanged candidate
                if 0 <= i < n - 1 and a[i] < a[i + 1]:
                    new_cand.add(i)
        candidates = sorted(new_cand)
    return time


# Problem 5: Mo's algorithm with Fenwick to maintain inversion count over current window
# We use block size ~ int(n**0.5)

class MoInversion:
    def __init__(self, arr: List[int]):
        self.orig = arr
        self.n = len(arr)
        self.comp_arr, self.compmap = compress(arr)
        self.maxv = max(self.comp_arr) if self.comp_arr else 0
        self.bit = Fenwick(self.maxv)
        self.freq = [0] * (self.maxv + 1)
        self.curr_inv = 0
        self.curr_l = 0
        self.curr_r = -1
        self.total = 0

    def add_right(self):
        x = self.comp_arr[self.curr_r]
        # count greater elements already in window
        greater = self.bit.range_sum(x + 1, self.maxv)
        self.curr_inv += greater
        self.bit.add(x, 1)
        self.freq[x] += 1

    def remove_right(self):
        x = self.comp_arr[self.curr_r]
        self.bit.add(x, -1)
        self.freq[x] -= 1
        greater = self.bit.range_sum(x + 1, self.maxv)
        self.curr_inv -= greater

    def add_left(self):
        x = self.comp_arr[self.curr_l]
        # when adding to left, count smaller elements in window
        smaller = self.bit.range_sum(1, x - 1)
        self.curr_inv += smaller
        self.bit.add(x, 1)
        self.freq[x] += 1

    def remove_left(self):
        x = self.comp_arr[self.curr_l]
        self.bit.add(x, -1)
        self.freq[x] -= 1
        smaller = self.bit.range_sum(1, x - 1)
        self.curr_inv -= smaller

    def process_query(self, L: int, R: int) -> int:
        # target inclusive indices L,R are 0-based
        while self.curr_r < R:
            self.curr_r += 1
            self.add_right()
        while self.curr_r > R:
            self.remove_right()
            self.curr_r -= 1
        while self.curr_l < L:
            self.remove_left()
            self.curr_l += 1
        while self.curr_l > L:
            self.curr_l -= 1
            self.add_left()
        return self.curr_inv


def inversion_queries(arr: List[int], queries: List[Tuple[int, int]]) -> List[int]:
    # queries are (l,r) 0-based inclusive
    if not arr:
        return [0] * len(queries)
    n = len(arr)
    block = max(1, int(n ** 0.5))
    idxs = list(range(len(queries)))
    idxs.sort(key=lambda i: (queries[i][0] // block, queries[i][1] if (queries[i][0] // block) % 2 == 0 else -queries[i][1]))
    mo = MoInversion(arr)
    ans = [0] * len(queries)
    for i in idxs:
        l, r = queries[i]
        ans[i] = mo.process_query(l, r)
    return ans


# Problem 6: minimal adjacent swaps to transform permutation A into B
# Map values of B to positions, create array P where P[i] = pos_in_B[A[i]], answer is inversion count of P

def min_adj_swaps_to_transform(A: List[int], B: List[int]) -> int:
    pos = {v: i + 1 for i, v in enumerate(B)}  # 1-based positions
    P = [pos[x] for x in A]
    return inversion_count(P)


if __name__ == "__main__":
    # quick tests
    a = [3, 1, 2]
    print('is_nearly_sorted [3,1,2] k=2 ->', is_nearly_sorted(a, 2))
    print('bubble swaps ->', bubble_swaps_needed(a))
    print('inversions after removal ->', inversions_after_removal(a))
    b = [1,2,3]
    print('queue overtakes time [1,2,3] ->', queue_overtake_time(b))
    arr = [3,1,4,2]
    queries = [(0,3),(1,2),(0,1)]
    print('inversion queries ->', inversion_queries(arr, queries))
    A = [3,1,2]
    B = [1,2,3]
    print('min swaps A->B ->', min_adj_swaps_to_transform(A,B))
