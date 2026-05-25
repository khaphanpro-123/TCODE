"""Solve two problems:
1) Sum of all numbers i in [1, n] whose digit sum equals k.
2) Sum of all numbers i in [1, n] with gcd(i, n) = 1.

The second problem uses the identity S = n * phi(n) / 2 for n > 1.
"""
from __future__ import annotations

from functools import lru_cache
from math import gcd
from typing import Tuple


def digit_sum(x: int) -> int:
    return sum(int(d) for d in str(x))


@lru_cache(maxsize=None)
def count_and_sum_digits(prefix_pos: int, current_sum: int, tight: bool, digits: Tuple[int, ...], target_sum: int) -> Tuple[int, int]:
    """Return (count, total_sum) for all suffixes from prefix_pos to end."""
    if prefix_pos == len(digits):
        return (1, 0) if current_sum == target_sum else (0, 0)

    limit = digits[prefix_pos] if tight else 9
    total_count = 0
    total_sum = 0
    multiplier = 10 ** (len(digits) - prefix_pos - 1)

    for dig in range(0, limit + 1):
        new_sum = current_sum + dig
        if new_sum > target_sum:
            continue

        next_tight = tight and (dig == limit)
        count, suffix_sum = count_and_sum_digits(prefix_pos + 1, new_sum, next_tight, digits, target_sum)
        total_count += count
        total_sum += dig * multiplier * count + suffix_sum

    return total_count, total_sum


def sum_with_digit_sum(n: int, k: int) -> int:
    """Sum all i in [1, n] such that digit_sum(i) == k."""
    if n <= 0 or k < 0:
        return 0

    digits = tuple(int(d) for d in str(n))
    count_and_sum_digits.cache_clear()

    # We include zero in DP, then subtract it if it is counted and not valid.
    _, total_sum = count_and_sum_digits(0, 0, True, digits, k)

    if k == 0:
        # only number 0 has digit sum 0; exclude it because we want [1, n]
        return 0
    return total_sum


def euler_phi(n: int) -> int:
    """Compute Euler's totient function phi(n)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    result = n
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1 if p == 2 else 2
    if x > 1:
        result -= result // x
    return result


def sum_coprime_with_n(n: int) -> int:
    """Sum all i in [1, n] such that gcd(i, n) == 1."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return n * euler_phi(n) // 2


def parse_ints_from_input() -> Tuple[int, int, int]:
    print("Enter n, k for digit-sum problem, and n for gcd problem.")
    print("If you want to use the same n for both problems, enter it twice.")
    values = input("Enter n k n_gcd (space-separated): ").strip().split()
    if len(values) != 3:
        raise ValueError("Expected exactly 3 integers.")
    return int(values[0]), int(values[1]), int(values[2])


def main() -> None:
    try:
        n_digit, k, n_gcd = parse_ints_from_input()
    except ValueError as exc:
        print(f"Input error: {exc}")
        return

    print(f"Sum of i in [1, {n_digit}] with digit sum = {k}:")
    print(sum_with_digit_sum(n_digit, k))

    print(f"Sum of i in [1, {n_gcd}] with gcd(i, {n_gcd}) = 1:")
    print(sum_coprime_with_n(n_gcd))


if __name__ == "__main__":
    main()
