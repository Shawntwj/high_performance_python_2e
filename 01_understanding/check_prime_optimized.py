import math

# Original version (from the book)
def check_prime_original(number):
    sqrt_number = math.sqrt(number)
    for i in range(2, int(sqrt_number) + 1):
        if (number / i).is_integer():  # Uses division + method call
            return False
    return True

# Optimized version 1: Use modulo instead of division
def check_prime_modulo(number):
    sqrt_number = math.sqrt(number)
    for i in range(2, int(sqrt_number) + 1):
        if number % i == 0:  # Faster: modulo operator
            return False
    return True

# Optimized version 2: Skip even numbers
def check_prime_skip_evens(number):
    if number == 2:
        return True
    if number < 2 or number % 2 == 0:
        return False
    sqrt_number = math.sqrt(number)
    for i in range(3, int(sqrt_number) + 1, 2):  # Skip even numbers
        if number % i == 0:
            return False
    return True

# Let's compare them
if __name__ == "__main__":
    test_number = 10_000_019

    print("Testing all three versions:")
    print(f"Original: {check_prime_original(test_number)}")
    print(f"Modulo: {check_prime_modulo(test_number)}")
    print(f"Skip evens: {check_prime_skip_evens(test_number)}")

    print("\nNow benchmark them with timeit:")
    print("Run these commands:")
    print("python -m timeit -s 'from check_prime_optimized import check_prime_original' 'check_prime_original(10_000_019)'")
    print("python -m timeit -s 'from check_prime_optimized import check_prime_modulo' 'check_prime_modulo(10_000_019)'")
    print("python -m timeit -s 'from check_prime_optimized import check_prime_skip_evens' 'check_prime_skip_evens(10_000_019)'")
