"""Compare Pure Python vs Cython performance

This file imports both the pure Python and Cython versions
and benchmarks them side-by-side.

Before running, you must compile the Cython extension:
    python setup_cython.py build_ext --inplace
"""

import time

# Try to import the compiled Cython module
try:
    import julia_cython
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False
    print("WARNING: Cython module not compiled!")
    print("Run: python setup_cython.py build_ext --inplace")
    print()

# Area of complex space to investigate
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -.42193


# Pure Python version (baseline)
def calculate_z_serial_purepython(maxiter, zs, cs):
    """Pure Python - no optimization"""
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output


def create_test_data(desired_width):
    """Create coordinate arrays for testing"""
    x_step = (x2 - x1) / desired_width
    y_step = (y1 - y2) / desired_width

    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step

    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    # Build coordinate lists
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    return zs, cs


def benchmark_version(name, func, maxiter, zs, cs, expected_sum):
    """Benchmark a specific implementation"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")

    start_time = time.time()
    output = func(maxiter, zs, cs)
    end_time = time.time()

    elapsed = end_time - start_time
    result_sum = sum(output)

    print(f"Time elapsed: {elapsed:.4f} seconds")
    print(f"Result sum: {result_sum}")
    print(f"Expected sum: {expected_sum}")
    print(f"Correct: {'✓' if result_sum == expected_sum else '✗'}")

    return elapsed


if __name__ == "__main__":
    print("Julia Set Performance Comparison")
    print("=" * 60)

    # Create test data
    desired_width = 1000
    max_iterations = 300
    expected_sum = 33219980

    print(f"\nGenerating test data ({desired_width}x{desired_width} grid)...")
    zs, cs = create_test_data(desired_width)
    print(f"Total elements: {len(zs):,}")

    # Benchmark Pure Python
    python_time = benchmark_version(
        "Pure Python (Baseline)",
        calculate_z_serial_purepython,
        max_iterations, zs, cs, expected_sum
    )

    if CYTHON_AVAILABLE:
        # Benchmark Cython basic version
        cython_time = benchmark_version(
            "Cython (Basic optimization)",
            julia_cython.calculate_z_serial_purepython,
            max_iterations, zs, cs, expected_sum
        )

        # Benchmark Cython optimized version
        # Convert to typed arrays for best performance
        import numpy as np
        zs_array = np.array(zs, dtype=np.complex128)
        cs_array = np.array(cs, dtype=np.complex128)

        cython_opt_time = benchmark_version(
            "Cython (Fully optimized)",
            julia_cython.calculate_z_cython_optimized,
            max_iterations, zs_array, cs_array, expected_sum
        )

        # Show speedup
        print(f"\n{'='*60}")
        print("SPEEDUP SUMMARY")
        print(f"{'='*60}")
        print(f"Pure Python:          {python_time:.4f}s  (baseline)")
        print(f"Cython (basic):       {cython_time:.4f}s  ({python_time/cython_time:.1f}x faster)")
        print(f"Cython (optimized):   {cython_opt_time:.4f}s  ({python_time/cython_opt_time:.1f}x faster)")
        print()
    else:
        print("\n" + "="*60)
        print("To see Cython performance:")
        print("1. Install Cython: pip install cython")
        print("2. Compile: python setup_cython.py build_ext --inplace")
        print("3. Run this script again")
        print("="*60)