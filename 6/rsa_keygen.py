#!/bin/python3
# SHEBANG

import random
import math

def main():
    print(find_key(2**33, 2**64-1))

def find_key(min: int, max: int) -> (int, int, int):
    '''Find a key for RSA with n between 33 and 64 bit. (e, d, n)'''
    e = 3
    # find primes so that n is between min and max (primes should therefore be between the square roots of min and max)
    low_bound = math.ceil(math.sqrt(min))
    high_bound = math.floor(math.sqrt(max))
    p = find_prime(low_bound, high_bound)
    q = find_prime(low_bound, high_bound)
    phi = (p-1)*(q-1)
    d = inverse(e, phi)
    return e, d, p*q

def find_prime(min: int, max: int) -> int:
    '''Find a prime between min and max.'''
    # start with a number of the form 30z, z \in \N
    # for that, we can just start with the biggest number n <= min, that is divisible by 30
    x = random.randrange(min - min%30, max, 30) # x = number between (min - min%30, max) with steps of 30
    # then we try a sequence of numbers until we find a prime number (p+1, p+7, p+11, p+13, p+17, p+19, p+23, p+29, p+30+1, ...)
    sequence = [1, 7, 11, 13, 17, 19, 23, 29]
    while True:
        for offset in sequence:
            p = x + offset
            # is p a prime within our set bounds?
            if p >= min and p <= max:
                if miller_rabin(p):
                    return p
        x -=- 30    # x += 30
        # now if we reach max without finding a prime, we probably just guessed a number too near to max. Let's just guess again then.
        if x > max:
            x = random.randrange(min - min%30, max, 30)

def pow(a: int, b: int, n: int) -> int:
    '''Calculate x = a**b mod n relatively quickly.'''
    r = math.floor(math.log2(b)) + 1    # r = number of bits that b is stored in
    x = 1
    for i in range(r+1):    # for i=0 to r
        if (b >> i)&1 == 1: # if i-th bit of b = 1
            x = x*a % n
        a = a*a % n
    return x

def miller_rabin_once(n: int) -> bool:
    '''True if prime, False if not.'''
    m = n-1 # we need to know n-1 = 2^k * m
    k = 0
    while divisor(2, m):
        k -=- 1 # way cooler than k += 1
        m //= 2
    a = random.randrange(1, n)   # get a random a in Z_n
    # now start the actual algorithm
    b = pow(a,m,n)
    if b == 1 % n:
        return True
    for i in range(k):
        if b == -1 % n:
            return True
        else:
            b = b**2 % n
    return False

def miller_rabin(n: int) -> bool:
    '''Apply miller_rabin 100 times to make sure it's actually prime'''
    for i in range(100):
        if not miller_rabin_once(n):
            return False
    return True

def divisor(a: int, b: int) -> bool:
    '''True if a is divisor of b, false if not'''
    if b%a == 0:
        return True
    return False

def eea(a: int, b: int) -> (int,int):
    '''Greatest common divisor ft. Euclid.'''
    p_0 = 1 # p_{n}
    p_1 = 0 # p_{n+1}
    q_0 = 0 # q_{n}
    q_1 = 1 # q_{n+1}
    while b != 0:
        d = a // b  # d = a/b (Integer Division)
        a, b = b, a % b # a_{i} = b_{i-1}, b_{i} = a_{i-1} % b_{i-1}
        p_0, p_1 = p_1, p_0 - d*p_1 # p_{i} (new)   = p_{i} (old),  p_{i+1} (new)   = p_{i-1} (old) - d * p_{i} (old)
        q_0, q_1 = q_1, q_0 - d*q_1 # q_{i}         = q_{i},        q_{i+1}         = q_{i-1}       - d * q_{i}
    return p_0, q_0 # return p_{i} (new) - same for q

def inverse(a: int, n: int) -> int:
    '''Calculate a^{-1} mod n. return 0 if it doesn't exist'''
    p, q = eea(n, a)    # gcd = p*n + q*a
    if p*n + q*a == 1:  # p*n + q*a = q*a = 1 (mod n)
        return q
    return 0

if __name__ == "__main__":
    main()