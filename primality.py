import math
import time

from solovay import solovay_strassen_test
from tqdm import tqdm

def is_power(n):
    if n <= 1:
        return False
    for base in range(2, int(math.sqrt(n)) + 1):
        exponent = 1
        power = base
        while power < n:
            exponent += 1
            power = base ** exponent
        if power == n:
            return True
    return False

def smallest_prime_not_dividing(n):
    def is_prime(p):
        if p < 2:
            return False
        for i in range(2, int(math.sqrt(p)) + 1):
            if p % i == 0:
                return False
        return True

    q = 2
    while True:
        if is_prime(q) and not any(n % (q**i - 1) == 0 for i in range(1, int((math.log(n) / math.log(2))**2) + 1)):
            return q
        q += 1

def check_ring_condition(n, q):
    for a in range(q - 1):
        left_side = (a**q + a)**n
        right_side = a**(n * q) + a
        if left_side % n != right_side % n:
            return False
    return True

def is_prime_using_algorithm(n):
    if n % 2 == 0:
        return n == 2
    if is_power(n):
        return False
    q = smallest_prime_not_dividing(n)
    return check_ring_condition(n, q)

def is_prime(n):
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    limit = math.isqrt(n)
    for i in range(5, limit+1, 6):
        if n % i == 0 or n % (i+2) == 0:
            return False
    return True

start_range = 2 ** 10000
end_range = start_range + 15

# Example usage
results_0 = []
results_1 = []
start = time.time()
for number in tqdm(range(start_range, end_range)):
    if solovay_strassen_test(number):
        results_0.append(1)
    else:
        results_0.append(0)
end = time.time()
print('algorithm 0 took', end - start, 'seconds')

start = time.time()
for number in tqdm(range(start_range, end_range)):
    if is_prime(number):
        results_1.append(1)
    else:
        results_1.append(0)
end = time.time()
print('algorithm 1 took', end - start, 'seconds')
