# Understanding `python -m timeit`

## The Command Broken Down

```bash
python -m timeit -s 'from timing_examples import add_numbers' 'add_numbers(5, 10)'
```

### Part by Part:

```
python -m timeit
│      │  └─── Module name: timeit (Python's built-in timer)
│      └─────── Flag: run a module as a script
└────────────── Python interpreter
```

```
-s 'from timing_examples import add_numbers'
│  └────────────────────────────────────────── Setup code (runs ONCE)
└───────────────────────────────────────────── Flag: --setup
```

```
'add_numbers(5, 10)'
└──────────────────── Code to time (runs MANY times)
```

## How It Works

### Step 1: Setup (runs ONCE)
```python
from timing_examples import add_numbers  # Import the function
```

### Step 2: Timing (runs MANY times - automatically determined)
```python
add_numbers(5, 10)  # ← This gets timed
add_numbers(5, 10)  # ← This gets timed
add_numbers(5, 10)  # ← This gets timed
# ... repeated 10,000,000 times!
```

### Step 3: Report the average
```
10000000 loops, best of 5: 30.3 nsec per loop
```

## Why This Matters

### ❌ WRONG WAY (timing includes import):
```bash
python -m timeit 'from timing_examples import add_numbers; add_numbers(5, 10)'
```
This times BOTH the import AND the function call!

### ✅ RIGHT WAY (only times the function):
```bash
python -m timeit -s 'from timing_examples import add_numbers' 'add_numbers(5, 10)'
```
This times ONLY the function call!

## Understanding the Output

```
10000000 loops, best of 5: 30.3 nsec per loop
│           │             │      └─── nanoseconds per loop
│           │             └────────── The fastest time
│           └──────────────────────── Repeated 5 times, took the best
└──────────────────────────────────── Function was called 10 million times
```

### Time Units:
- **nsec** = nanoseconds (billionths of a second) - SUPER FAST
- **usec** = microseconds (millionths of a second) - FAST
- **msec** = milliseconds (thousandths of a second) - OKAY
- **sec** = seconds - SLOW

## Real Examples from Our Tests:

### Fast: add_numbers
```
10000000 loops, best of 5: 30.3 nsec per loop
```
So fast it ran 10 MILLION times!

### Slower: slow_loop
```
10000 loops, best of 5: 23.2 usec per loop
```
Slower, so it only ran 10 THOUSAND times

### Even Slower: check_prime(10_000_019)
```
2000 loops, best of 5: 111 usec per loop
```
Much slower, only ran 2 THOUSAND times

## Common Usage Patterns

### 1. Time a simple function
```bash
python -m timeit -s 'from myfile import myfunction' 'myfunction()'
```

### 2. Time with different arguments
```bash
python -m timeit -s 'from myfile import myfunction' 'myfunction(100)'
python -m timeit -s 'from myfile import myfunction' 'myfunction(1000)'
python -m timeit -s 'from myfile import myfunction' 'myfunction(10000)'
```

### 3. Time with setup data
```bash
python -m timeit -s 'from myfile import myfunction; data = [1,2,3,4,5]' 'myfunction(data)'
```

### 4. Specify number of runs manually
```bash
python -m timeit -n 1000 -s 'from myfile import slow_function' 'slow_function()'
#                 └─ run exactly 1000 times
```

## Quick Reference

| Flag | What it does | Example |
|------|--------------|---------|
| `-s` | Setup code (runs once) | `-s 'import math'` |
| `-n` | Number of times to run | `-n 1000` |
| `-r` | Number of repeats | `-r 10` (default is 5) |
| `-v` | Verbose output | `-v` |

## Try It Yourself!

```bash
# Go to the 01_understanding directory
cd /Users/shawnteo/Documents/GitHub/high_performance_python_2e/01_understanding

# Time the examples
python -m timeit -s 'from timing_examples import add_numbers' 'add_numbers(5, 10)'
python -m timeit -s 'from timing_examples import slow_loop' 'slow_loop()'
python -m timeit -s 'from timing_examples import check_prime' 'check_prime(97)'

# Compare optimized versions from check_prime_optimized.py
python -m timeit -s 'from check_prime_optimized import check_prime_original' 'check_prime_original(10_000_019)'
python -m timeit -s 'from check_prime_optimized import check_prime_skip_evens' 'check_prime_skip_evens(10_000_019)'
```

Now you can see which version is faster! 🚀
