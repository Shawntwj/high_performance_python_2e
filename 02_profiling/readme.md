i learnt alot this ch in high perf python by micha can you help verify what i learnt 

profiling is necessary to see the performance of the code this is impt because python is an interpreted language and dynamically typed 

there is more layers 

code -> bytecode -> compiled -> machine code 

and as GC is not immediate we may not always know what is going on under the hood 

and because of the GIL it can be quite slow as it is always single process

thus profiling is needed generally the flow would go like this 

1. use python's timeit module on the code you want to test timeit is in built and will run experiments for you unless you specify yourself then slowly isolate down to which funcs are causing potential problems 
2. after finding out on a surface lvl analysis use cprofile another in built tool thus will allow you to see which functions are slow how many hits how long do they take? etc 
2b. can visualize using snakeviz by using cprofile to generate a statfile if you want buy in or better understanding on which funcs are CPU intensive 
3. use line profiler using @profile and kernprof to see a more detailed table of which line is causing problems 
4. based on your understanding of the code and how python works and interacts with the CPU do the following 
5a. if you are processing a list and that list is homogeous consider vectorizing it using a library like numpy as vectorizing takes advantage of the SIMD unit in the CPU to calculate multiple operations in one unit 
5b. if the code doesn't rely on any python libraries consider compiling it to machine code using C or Cython or numba as compiled code is just one layer away from machine code then you can call that to be used in your python code once compiled
5c. if the output is not dependent on each other and can be parrallalized consider multi processing in different CPUs not multi threading because of the GIL 
5d. use efficient algos or data structures or in built libraries for the task e.g using hashmap for lookups or sum() for add as most of these are in C they don't have to inteprete the variable is what type and then lookup the variable they just compile quicker 

for memory profiling we use the 
1. memory_profiler to test the whole code can use flags to call out long running funcs if space of machine is small 
2. mprof to show how much RAM and memory the funcs are using 

the trade off for memory is that we always want to see if we can use less or more RAM to save CPU cycles  

use unit tests whenver possible to ensure optimizations don't break the code 

use the @profile tag to be able to scan with kernprof and memory_profiler 

use a no-op decorator to ensure that we can continue adding this in tests

1. Basic Timing (time module)

# Run with built-in time.time() decorator
python julia1_decorator.py
2. timeit Module

# Quick one-liner timing (from command line)
python -m timeit -s "from julia1 import calculate_z_serial_purepython" "calculate_z_serial_purepython(300, zs, cs)"

# Or use timeit in a script
python -m timeit "sum(range(1000))"
3. cProfile (Function-level profiling)

# Profile and output to terminal
python -m cProfile julia1_nopil.py

# Profile and save to file for later analysis
python -m cProfile -o profile.stats julia1_nopil.py

# View the saved stats file
python seestats.py

# Or analyze interactively
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats()"
4. Visualize cProfile with SnakeViz

# First install snakeviz
pip install snakeviz

# Generate stats file then visualize
python -m cProfile -o profile.stats julia1_nopil.py
snakeviz profile.stats
5. line_profiler (Line-by-line profiling)

# First install line_profiler
pip install line_profiler

# Run with kernprof (outputs to terminal with -v flag)
kernprof -l -v julia1_lineprofiler.py

# Save results to .lprof file (view later)
kernprof -l julia1_lineprofiler.py
python -m line_profiler julia1_lineprofiler.py.lprof

# Profile specific functions only (add @profile decorator to functions)
kernprof -l -v julia1_lineprofiler2.py
6. memory_profiler (Memory usage)

# First install memory_profiler
pip install memory_profiler

# Run with memory profiling (line-by-line)
python -m memory_profiler julia1_memoryprofiler.py

# Using no-op decorator pattern (runs with or without profiler)
python noop_profile_demo.py                              # Normal run
python -m memory_profiler noop_profile_demo.py           # With profiling
7. mprof (Memory over time visualization)

# First install memory_profiler (includes mprof)
pip install memory_profiler matplotlib

# Run and generate memory plot data
mprof run julia1_memoryprofiler.py

# View the plot
mprof plot

# Clean previous runs
mprof clean
8. dis Module (Bytecode inspection)

# View Python bytecode
python dis_sample.py

# Or from command line
python -m dis your_script.py
9. Cython (Compile to C)

# First install Cython
pip install cython

# Build the Cython extension
python setup_cython.py build_ext --inplace

# Then run your optimized code
python julia_compare.py
Quick Reference Workflow

# 1. Start with timing
python julia1_decorator.py

# 2. Find slow functions
python -m cProfile -o profile.stats julia1_nopil.py
snakeviz profile.stats

# 3. Find slow lines
kernprof -l -v julia1_lineprofiler.py

# 4. Check memory usage
python -m memory_profiler julia1_memoryprofiler.py
mprof run julia1_memoryprofiler.py && mprof plot

# 5. Optimize and compare
python julia_compare.py
Save this as a reference! All commands are ready to run from the 02_profiling/ directory.