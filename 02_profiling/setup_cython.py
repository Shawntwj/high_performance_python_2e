"""Setup script to compile the Cython extension

To compile, run:
    python setup_cython.py build_ext --inplace

This will create a compiled .so (Linux/Mac) or .pyd (Windows) file
that can be imported like a normal Python module.
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Define the extension module
extensions = [
    Extension(
        "julia_cython",                    # Module name
        ["julia_cython.pyx"],              # Source file
        include_dirs=[np.get_include()],   # Include NumPy headers
    )
]

setup(
    name="julia_cython",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",          # Use Python 3 syntax
            'boundscheck': False,           # Disable bounds checking for speed
            'wraparound': False,            # Disable negative indexing for speed
            'cdivision': True,              # Use C division (faster)
        }
    ),
)