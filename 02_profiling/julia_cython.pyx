"""Cython optimized Julia set generator
This is a .pyx file that will be compiled to C
"""

# Import C math functions for better performance
from libc.math cimport abs as c_abs

# Cython function with type declarations
def calculate_z_serial_purepython(int maxiter, list zs, list cs):
    """Calculate output list using Julia update rule - Cython optimized"""
    cdef int i, n  # Changed to int to match maxiter type
    cdef double complex z, c
    cdef int[:] output_view
    cdef list output = [0] * len(zs)

    # Process each point
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]

        # Hot loop - this is where Cython optimization matters most
        while n < maxiter and c_abs(z.real * z.real + z.imag * z.imag) < 4.0:
            z = z * z + c
            n += 1
        output[i] = n

    return output


# Even more optimized version using C arrays
def calculate_z_cython_optimized(int maxiter, double complex[:] zs, double complex[:] cs):
    """Fully optimized Cython version using typed memoryviews"""
    cdef int i, n, length
    cdef double complex z, c

    length = len(zs)
    # Use a simple list - no need for memoryview overhead
    output = [0] * length

    # No Python object overhead in this loop
    for i in range(length):
        n = 0
        z = zs[i]
        c = cs[i]

        # Optimized: abs(z) < 2 is same as abs(z)^2 < 4
        # Avoid sqrt by comparing squared magnitude
        while n < maxiter and (z.real * z.real + z.imag * z.imag) < 4.0:
            z = z * z + c
            n += 1

        output[i] = n

    return output