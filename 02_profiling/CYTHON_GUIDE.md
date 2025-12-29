# Cython Optimization Guide for Julia Set

This guide shows how to convert Pure Python to Cython for major performance improvements.

## Files Created

1. **julia_cython.pyx** - Cython source code (compiled to C)
2. **setup_cython.py** - Build script to compile the Cython code
3. **julia_compare.py** - Benchmark script comparing Python vs Cython
4. **CYTHON_GUIDE.md** - This file

## Quick Start

### Step 1: Install Cython
```bash
pip install cython
```

### Step 2: Compile the Cython Extension
```bash
cd 02_profiling
python setup_cython.py build_ext --inplace
```

This creates a compiled `.so` (Mac/Linux) or `.pyd` (Windows) file.

### Step 3: Run the Comparison
```bash
python julia_compare.py
```

## Understanding the Code

### Pure Python (Slow)
```python
def calculate_z_serial_purepython(maxiter, zs, cs):
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:  # Python overhead here!
            z = z * z + c
            n += 1
        output[i] = n
    return output
```

**Why slow:**
- All variables are Python objects (overhead)
- Type checking on every operation
- `abs()` is a Python function call
- 34 million iterations with Python overhead

### Cython (Fast) - Key Differences

```cython
def calculate_z_serial_purepython(int maxiter, list zs, list cs):
    cdef unsigned int i, n              # ← C integers, not Python objects
    cdef double complex z, c            # ← C complex numbers

    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]

        # abs(z) < 2 is same as abs(z)^2 < 4, avoid sqrt
        while n < maxiter and (z.real*z.real + z.imag*z.imag) < 4.0:
            z = z * z + c                # ← Native C operations
            n += 1
        output[i] = n
    return output
```

**Why fast:**
- `cdef` declares C variables (no Python overhead)
- Type known at compile time (no type checking)
- Math operations compile to native CPU instructions
- Loop runs at C speed

## Key Cython Syntax

### 1. Type Declarations

```cython
cdef int n                    # C integer
cdef double x                 # C double (float)
cdef double complex z         # C complex number
cdef list my_list             # Python list (still has overhead)
```

### 2. Function Arguments

```python
# Pure Python
def func(maxiter, zs, cs):
    pass

# Cython - specify types
def func(int maxiter, list zs, list cs):
    pass
```

### 3. Typed Memoryviews (Advanced)

```cython
# Instead of Python list
def func(double complex[:] zs, double complex[:] cs):
    # zs and cs are now efficient C arrays
    # Much faster than Python lists
```

### 4. C Math Functions

```cython
from libc.math cimport abs as c_abs

# Use C's abs instead of Python's abs
while c_abs(z) < 2:
    pass
```

## Performance Optimizations in the Code

### Optimization 1: Use `cdef` for Loop Variables
```python
# Slow (Python int objects)
for i in range(len(zs)):
    n = 0

# Fast (C integers)
cdef unsigned int i, n
for i in range(len(zs)):
    n = 0
```

### Optimization 2: Avoid `abs()` Overhead
```python
# Slower - calls abs() which involves sqrt
while abs(z) < 2:
    pass

# Faster - avoid square root
# abs(z) < 2  is same as  abs(z)^2 < 4
while (z.real * z.real + z.imag * z.imag) < 4.0:
    pass
```

### Optimization 3: Use Typed Memoryviews
```cython
# Slower - Python list with object overhead
def func(list zs):
    z = zs[i]  # Python object access

# Faster - Direct memory access
def func(double complex[:] zs):
    z = zs[i]  # C array access, no overhead
```

## Expected Performance

For a 1000×1000 grid with 300 iterations:

| Version               | Time    | Speedup |
|-----------------------|---------|---------|
| Pure Python           | ~33s    | 1x      |
| Cython (basic)        | ~5s     | 6-7x    |
| Cython (optimized)    | ~0.5s   | 60-70x  |
| NumPy (vectorized)    | ~0.1s   | 300x+   |

## Compiler Directives Explained

In `setup_cython.py`:

```python
compiler_directives={
    'language_level': "3",      # Use Python 3 syntax
    'boundscheck': False,       # Don't check array bounds (faster, less safe)
    'wraparound': False,        # Don't support negative indexing (faster)
    'cdivision': True,          # Use C division rules (faster)
}
```

**Trade-off:** These make code faster but remove safety checks!

## How Compilation Works

```
julia_cython.pyx  (Cython code)
       ↓
   [Cython Compiler]
       ↓
julia_cython.c    (Generated C code - you can look at this!)
       ↓
   [C Compiler (gcc/clang)]
       ↓
julia_cython.so   (Compiled binary you can import in Python)
```

## Using the Compiled Module

After compilation:

```python
import julia_cython

# Use it like a normal Python module!
output = julia_cython.calculate_z_serial_purepython(maxiter, zs, cs)
```

## Common Errors

### Error: "Cannot find cython"
**Solution:** `pip install cython`

### Error: "No C compiler found"
**Solution:**
- **Mac:** Install Xcode Command Line Tools: `xcode-select --install`
- **Linux:** `sudo apt-get install build-essential`
- **Windows:** Install Visual Studio Build Tools

### Error: "ImportError: No module named julia_cython"
**Solution:** Run the compile step first:
```bash
python setup_cython.py build_ext --inplace
```

## Next Steps

1. **Try it:** Compile and run the comparison
2. **Experiment:** Modify `julia_cython.pyx` and recompile
3. **Profile:** Use line_profiler on Cython code to find remaining bottlenecks
4. **Compare:** Try NumPy vectorization for even better performance

## Further Reading

- [Cython Documentation](https://cython.readthedocs.io/)
- [Cython Tutorial](https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html)
- Check later chapters in the book for more optimization techniques!