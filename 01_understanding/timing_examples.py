"""
Examples to understand timeit command
"""

# Example 1: Simple function
def add_numbers(a, b):
    return a + b

# Example 2: Slower function
def slow_loop():
    total = 0
    for i in range(1000):
        total += i
    return total

# Example 3: The check_prime function
import math

def check_prime(number):
    sqrt_number = math.sqrt(number)
    for i in range(2, int(sqrt_number) + 1):
        if number % i == 0:
            return False
    return True

if __name__ == "__main__":
    print("To time these functions, use these commands:")
    print()
    print("1. Time add_numbers:")
    print("   python -m timeit -s 'from timing_examples import add_numbers' 'add_numbers(5, 10)'")
    print()
    print("2. Time slow_loop:")
    print("   python -m timeit -s 'from timing_examples import slow_loop' 'slow_loop()'")
    print()
    print("3. Time check_prime:")
    print("   python -m timeit -s 'from timing_examples import check_prime' 'check_prime(97)'")
    print()
    print("Let me show you what each part does...")
