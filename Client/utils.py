import math
import random


def gen_mprime(p: int):
    while True:
        if math.gcd(p, b := random.randrange(2, p)) == 1:
            return b


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