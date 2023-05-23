import json
import random
import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def jacobi_symbol(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1
    result = 1
    if a < 0:
        a = -a
        if n % 4 == 3:
            result = -result
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    return 0

def solovay_strassen_test(n, k=10):
    if n == 2 or n == 3:
        return 1
    if n % 2 == 0 or n == 1:
        return 0

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, (n - 1) // 2, n)
        j = jacobi_symbol(a, n) % n
        if x != j:
            return 0
    return 1

def test_range(lower, upper, k=15):
    results = {}
    for n in range(lower, upper + 1):
        results[n] = solovay_strassen_test(n, k)
    return results

if __name__ == '__main__':
    lower_bound = int(sys.argv[1])
    upper_bound = int(sys.argv[2])
    results = test_range(lower_bound, upper_bound)

    with open('results.json', 'w') as file:
        json.dump(results, file)

    print(f"Results saved to 'results.json'. 0 represents compositeness and 1 represents primality.")
