"""Solutions for problems 2..8 from user's request.

Provide functions and a simple CLI for quick testing.
"""
from __future__ import annotations

from math import gcd, isqrt
from functools import lru_cache
from typing import List

MOD = 10**9 + 7

# Problem 2: Sum of Fibonacci numbers <= n
# Identity: sum_{i=1..k} F_i = F_{k+2} - 1

def sum_fib_upto(n: int) -> int:
    if n < 1:
        return 0
    a, b = 0, 1
    # build fibs until > n
    fibs = []
    while b <= n:
        fibs.append(b)
        a, b = b, a + b
    if not fibs:
        return 0
    # sum of fibs up to largest F_k <= n is F_{k+2} - 1
    # compute F_{k+2} where k = len(fibs)
    # We currently have F_1..F_k in fibs; compute two more
    if len(fibs) >= 1:
        f_k_plus_1 = fibs[-1] + (fibs[-2] if len(fibs) >= 2 else 0)
    else:
        f_k_plus_1 = 1
    f_k_plus_2 = fibs[-1] + f_k_plus_1
    return f_k_plus_2 - 1


# Problem 3: Sum of perfect numbers <= n
# We use the known list of even perfect numbers (from Mersenne primes).
KNOWN_PERFECT_NUMBERS = [
    6,
    28,
    496,
    8128,
    33550336,
    8589869056,
    137438691328,
    2305843008139952128,  # >1e18, kept for completeness
]


def sum_perfects_upto(n: int) -> int:
    total = 0
    for x in KNOWN_PERFECT_NUMBERS:
        if x <= n:
            total += x
    return total


# Problem 4: LCM(1..n) modulo MOD
# lcm(1..n) = product_{primes p <= n} p^{floor(log_p n)}

def primes_upto(n: int) -> List[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:n+1:step] = b"\x00" * (((n - start) // step) + 1)
    return [i for i, isprime in enumerate(sieve) if isprime]


def lcm_1_to_n_mod(n: int, mod: int = MOD) -> int:
    if n < 1:
        return 1
    res = 1
    for p in primes_upto(n):
        # compute exponent e = floor(log_p n)
        e = 1
        pp = p
        while pp * p <= n:
            pp *= p
            e += 1
        res = res * pow(p, e, mod) % mod
    return res


# Problem 5: Sum_{i=1..n} i^k mod p, with large n and k
# We'll use Lagrange interpolation: the polynomial S(n) has degree k+1
# Compute y[i] = sum_{j=1..i} j^k for i=0..k+1 and interpolate at n.


def modinv(a: int, mod: int = MOD) -> int:
    return pow(a, mod - 2, mod)


def sum_of_powers(n: int, k: int, mod: int = MOD) -> int:
    if n == 0:
        return 0
    if k == 0:
        return n % mod
    # If n <= k+1 compute directly
    limit = k + 1
    if n <= limit:
        s = 0
        for i in range(1, n + 1):
            s = (s + pow(i, k, mod)) % mod
        return s

    # compute y[0..limit] where y[m] = sum_{i=1..m} i^k
    y = [0] * (limit + 1)
    for i in range(1, limit + 1):
        y[i] = (y[i - 1] + pow(i, k, mod)) % mod

    # Precompute factorials
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % mod
    invfact = [1] * (limit + 1)
    invfact[limit] = modinv(fact[limit], mod)
    for i in range(limit, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    # Lagrange interpolation at point n
    # Compute prefix and suffix products for (n - x_i)
    pre = [1] * (limit + 1)
    for i in range(0, limit + 1):
        if i == 0:
            pre[i] = (n - 0) % mod
        else:
            pre[i] = pre[i - 1] * ((n - i) % mod) % mod
    suf = [1] * (limit + 1)
    for i in range(limit, -1, -1):
        if i == limit:
            suf[i] = (n - limit) % mod
        else:
            suf[i] = suf[i + 1] * ((n - i) % mod) % mod

    ans = 0
    for i in range(0, limit + 1):
        # numerator = prod_{j != i} (n - j) = pre[i-1]*suf[i+1]
        if i == 0:
            numer = suf[1]
        elif i == limit:
            numer = pre[limit - 1]
        else:
            numer = pre[i - 1] * suf[i + 1] % mod
        denom = (invfact[i] * invfact[limit - i]) % mod
        sign = -1 if ((limit - i) % 2) else 1
        term = y[i] * numer % mod * denom % mod
        if sign == -1:
            ans = (ans - term) % mod
        else:
            ans = (ans + term) % mod
    return ans


# Problem 6: Sum of numbers in 1..n divisible by at least one of a_i
# Using inclusion-exclusion. For a subset with lcm d, sum of multiples = d * m*(m+1)/2 where m=n//d

def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def sum_multiples(n: int, d: int) -> int:
    m = n // d
    return d * m * (m + 1) // 2


def sum_divisible_by_any(n: int, arr: List[int]) -> int:
    from itertools import combinations
    arr = [x for x in arr if x > 0]
    m = len(arr)
    if m == 0:
        return 0
    total = 0
    for r in range(1, m + 1):
        for comb in combinations(arr, r):
            cur = 1
            overflow = False
            for x in comb:
                cur = lcm(cur, x)
                if cur > n:
                    overflow = True
                    break
            if overflow or cur == 0:
                continue
            s = sum_multiples(n, cur)
            if r % 2 == 1:
                total += s
            else:
                total -= s
    return total


# Problem 7: Count occurrences of digit d in 1..n

def count_digit_occurrences(n: int, d: int) -> int:
    if n <= 0:
        return 0
    if d < 0 or d > 9:
        raise ValueError("d must be in 0..9")
    count = 0
    factor = 1
    while factor <= n:
        lower = n - (n // factor) * factor
        cur = (n // factor) % 10
        higher = n // (factor * 10)
        if d != 0:
            if cur > d:
                count += (higher + 1) * factor
            elif cur == d:
                count += higher * factor + lower + 1
            else:
                count += higher * factor
        else:
            # digit 0: leading zeros not allowed
            if higher == 0:
                # no full cycles
                pass
            else:
                if cur > 0:
                    count += (higher - 1 + 1) * factor
                elif cur == 0:
                    count += (higher - 1) * factor + lower + 1
    
        factor *= 10
    return count


# Problem 8: Sum LCM(i, n) for i=1..n modulo MOD
# Use formula grouping by m = n/g where g|n: sum = n * ( sum_{m|n} sum_{j coprime to m} j )
# and sum_{j coprime to m} j = 1 if m==1 else m*phi(m)/2

def euler_phi(n: int) -> int:
    if n <= 0:
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


def sum_lcm_with_n(n: int, mod: int = MOD) -> int:
    if n <= 0:
        return 0
    # compute divisors
    divs = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
        i += 1
    total = 0
    for m in divs:
        if m == 1:
            s = 1
        else:
            s = m * euler_phi(m) // 2
        total = (total + s) % mod
    return n % mod * total % mod


if __name__ == "__main__":
    # quick manual tests
    print("Problem 2: sum fibs <= 100 ->", sum_fib_upto(100))
    print("Problem 3: sum perfects <= 100000 ->", sum_perfects_upto(100000))
    print("Problem 4: lcm(1..10) mod ->", lcm_1_to_n_mod(10))
    print("Problem 5: sum i^3 for i=1..10 ->", sum_of_powers(10, 3))
    print("Problem 6: sum divisible by [2,3] up to 10 ->", sum_divisible_by_any(10, [2,3]))
    print("Problem 7: occurrences of digit 1 in 1..13 ->", count_digit_occurrences(13, 1))
    print("Problem 8: sum lcm(i, 7) ->", sum_lcm_with_n(7))
