#include <iostream>
#include <fstream>
#include <random>
#include <unordered_map>
#include <string>
#include <cstdlib>
#include <cmath>
#include "json.hpp"

using json = nlohmann::json;

int gcd(int a, int b) {
    while (b) {
        a %= b;
        std::swap(a, b);
    }
    return a;
}

int jacobi_symbol(int a, int n) {
    if (a == 0) return 0;
    if (a == 1) return 1;

    int result = 1;
    if (a < 0) {
        a = -a;
        if (n % 4 == 3) result = -result;
    }

    while (a != 0) {
        while (a % 2 == 0) {
            a /= 2;
            if (n % 8 == 3 || n % 8 == 5) result = -result;
        }
        std::swap(a, n);
        if (a % 4 == 3 && n % 4 == 3) result = -result;
        a %= n;
    }
    return n == 1 ? result : 0;
}

int solovay_strassen_test(int n, int k = 10) {
    if (n == 2 || n == 3) return 1;
    if (n % 2 == 0 || n == 1) return 0;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(2, n - 2);

    for (int i = 0; i < k; ++i) {
        int a = dis(gen);
        int x = static_cast<int>(std::pow(a, (n - 1) / 2)) % n;
        int j = jacobi_symbol(a, n) % n;
        if (x != j) return 0;
    }
    return 1;
}

std::unordered_map<int, int> test_range(int lower, int upper, int k = 15) {
    std::unordered_map<int, int> results;
    for (int n = lower; n <= upper; ++n) {
        results[n] = solovay_strassen_test(n, k);
    }
    return results;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " lower_bound upper_bound" << std::endl;
        return 1;
    }

    int lower_bound = std::stoi(argv[1]);
    int upper_bound = std::stoi(argv[2]);

    auto results = test_range(lower_bound, upper_bound);

    std::ofstream file("results.json");
    json j(results);
    file << j.dump();
    file.close();

    std::cout << "Results saved to 'results.json'. 0 represents compositeness and 1 represents primality." << std::endl;

    return 0;
}
