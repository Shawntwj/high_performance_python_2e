"""
Demonstrating why timeit uses different loop counts
"""
import time

# SUPER FAST function
def super_fast():
    return 1 + 1

# FAST function
def fast():
    total = 0
    for i in range(100):
        total += i
    return total

# SLOW function
def slow():
    total = 0
    for i in range(10000):
        total += i
    return total

# VERY SLOW function
def very_slow():
    time.sleep(0.01)  # Sleep for 10 milliseconds
    return "done"

if __name__ == "__main__":
    print("Run these commands and watch the loop count:")
    print()
    print("1. Super fast (will run ~10,000,000 times):")
    print("   python -m timeit -s 'from why_different_loops import super_fast' 'super_fast()'")
    print()
    print("2. Fast (will run ~100,000 times):")
    print("   python -m timeit -s 'from why_different_loops import fast' 'fast()'")
    print()
    print("3. Slow (will run ~1,000 times):")
    print("   python -m timeit -s 'from why_different_loops import slow' 'slow()'")
    print()
    print("4. Very slow (will run ~10 times):")
    print("   python -m timeit -s 'from why_different_loops import very_slow' 'very_slow()'")
    print()
    print("Notice: timeit automatically adjusts the loop count!")