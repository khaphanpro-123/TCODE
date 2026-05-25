"""Sliding window exercises: problems 1..8.

Functions:
- max_sum_exact_k
- min_sum_exact_k
- min_len_subarray_with_sum_at_least_k (positive numbers)
- longest_with_at_most_k_evens
- max_average_subarray_at_least_k
- longest_all_distinct
- longest_at_most_k_distinct
- count_subarrays_sum_k (handles negatives)

Simple CLI tests at bottom.
"""
from __future__ import annotations
from typing import List, Sequence, Tuple, Hashable


def max_sum_exact_k(arr: Sequence[int], k: int) -> int:
    n = len(arr)
    if k > n or k <= 0:
        raise ValueError("k must be in 1..n")
    s = sum(arr[:k])
    best = s
    for i in range(k, n):
        s += arr[i] - arr[i - k]
        if s > best:
            best = s
    return best


def min_sum_exact_k(arr: Sequence[int], k: int) -> int:
    n = len(arr)
    if k > n or k <= 0:
        raise ValueError("k must be in 1..n")
    s = sum(arr[:k])
    best = s
    for i in range(k, n):
        s += arr[i] - arr[i - k]
        if s < best:
            best = s
    return best


def min_len_subarray_with_sum_at_least_k(arr: Sequence[int], k: int) -> int:
    # arr contains positive integers
    n = len(arr)
    left = 0
    cur = 0
    best = n + 1
    for right in range(n):
        cur += arr[right]
        while cur >= k:
            best = min(best, right - left + 1)
            cur -= arr[left]
            left += 1
    return -1 if best == n + 1 else best


def longest_with_at_most_k_evens(arr: Sequence[int], k: int) -> int:
    n = len(arr)
    left = 0
    evens = 0
    best = 0
    for right in range(n):
        if arr[right] % 2 == 0:
            evens += 1
        while evens > k:
            if arr[left] % 2 == 0:
                evens -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def max_average_subarray_at_least_k(arr: Sequence[int], k: int, eps: float = 1e-5) -> float:
    # binary search on average
    lo, hi = min(arr), max(arr)
    def check(mid: float) -> bool:
        n = len(arr)
        # transform and check if exists subarray length >= k with sum >= 0
        prefix = [0.0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + (arr[i] - mid)
        min_prefix = 0.0
        for j in range(k, n + 1):
            if prefix[j] - min_prefix >= 0:
                return True
            min_prefix = min(min_prefix, prefix[j - k + 1])
        return False
    while hi - lo > eps:
        mid = (lo + hi) / 2.0
        if check(mid):
            lo = mid
        else:
            hi = mid
    return lo


def longest_all_distinct(seq: Sequence[Hashable]) -> int:
    last = {}
    left = 0
    best = 0
    for i, x in enumerate(seq):
        if x in last and last[x] >= left:
            left = last[x] + 1
        last[x] = i
        best = max(best, i - left + 1)
    return best


def longest_at_most_k_distinct(s: Sequence[Hashable], k: int) -> int:
    from collections import defaultdict
    cnt = defaultdict(int)
    left = 0
    distinct = 0
    best = 0
    for right, ch in enumerate(s):
        if cnt[ch] == 0:
            distinct += 1
        cnt[ch] += 1
        while distinct > k:
            cnt[s[left]] -= 1
            if cnt[s[left]] == 0:
                distinct -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def count_subarrays_sum_k(arr: Sequence[int], k: int) -> int:
    from collections import defaultdict
    pref = 0
    cnt = defaultdict(int)
    cnt[0] = 1
    ans = 0
    for x in arr:
        pref += x
        ans += cnt.get(pref - k, 0)
        cnt[pref] += 1
    return ans


if __name__ == "__main__":
    # quick tests
    a = [1,2,3,4,5]
    print('P1 max sum k=2 ->', max_sum_exact_k(a,2))
    print('P2 min sum k=2 ->', min_sum_exact_k(a,2))
    print('P3 min len sum>=7 ->', min_len_subarray_with_sum_at_least_k(a,7))
    print('P4 longest at most 1 even ->', longest_with_at_most_k_evens([1,2,4,5,6],1))
    print('P5 max avg len>=2 ->', max_average_subarray_at_least_k(a,2))
    print('P6 longest all distinct ->', longest_all_distinct([1,2,1,3,4]))
    print('P7 longest at most 2 distinct ->', longest_at_most_k_distinct('eceba',2))
    print('P8 count sum k=5 ->', count_subarrays_sum_k([1,4,2,3,1],5))
