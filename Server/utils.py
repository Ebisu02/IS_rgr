import random
import math


def get_prime(l: int, r: int) -> int:
    while True:
        p = random.randint(l, r)
        if is_prime(p):
            return p


def is_prime(p: int, trials: int=64) -> bool:
    if p == 1 or not (p & 1):
        return False
    if p == 2 or p == 3 or p == 5 or p == 7:
        return True
    for _ in range(trials):
        a = random.randint(2, p - 1)
        if ext_gcd(a, (p - 1), p) != 1 or math.gcd(p, a) > 1:
            return False
    return True


def ext_gcd(a: int, x: int, p: int) -> int:
    if p == 0 or x < 0:
        raise ValueError(f"Error in ext_gcd() func, vars: {a = }, {x = }, {p = }")
    result = 1
    a = a % p
    if a == 0:
        return 0
    while x > 0:
        if x & 1 == 1:
            result = (result * a) % p
        a = (a ** 2) % p
        x >>= 1
    return result