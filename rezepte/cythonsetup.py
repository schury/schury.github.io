from setuptools import setup
from Cython.Build import cythonize

setup(
    name = "myapp",
    ext_modules = cythonize("test.py")
)

