"""
Demo: No-op @profile decorator
This file can be run with OR without memory_profiler!

Try both:
  1. python noop_profile_demo.py           (uses no-op decorator)
  2. python -m memory_profiler noop_profile_demo.py   (uses real profiler)
"""

# No-op @profile decorator - only activates if memory_profiler isn't running
if 'profile' not in dir():
    print("NOTE: Using no-op @profile decorator (memory_profiler not active)")
    def profile(func):
        """Dummy decorator that does nothing"""
        return func
else:
    print("NOTE: Using real @profile from memory_profiler")


@profile
def allocate_small_list():
    """Allocate a small list - should use minimal memory"""
    data = [i for i in range(1000)]
    return sum(data)


@profile
def allocate_large_list():
    """Allocate a large list - should use more memory"""
    data = [i for i in range(1_000_000)]
    return sum(data)


@profile
def create_nested_structure():
    """Create nested lists - watch memory grow"""
    outer = []
    for i in range(100):
        inner = [j * i for j in range(10000)]
        outer.append(inner)
    return len(outer)


def main():
    print("\n=== Running memory profiling demo ===\n")

    print("1. Allocating small list...")
    result1 = allocate_small_list()
    print(f"   Sum: {result1}")

    print("\n2. Allocating large list...")
    result2 = allocate_large_list()
    print(f"   Sum: {result2}")

    print("\n3. Creating nested structure...")
    result3 = create_nested_structure()
    print(f"   Lists created: {result3}")

    print("\n=== Demo complete ===")


if __name__ == "__main__":
    main()
