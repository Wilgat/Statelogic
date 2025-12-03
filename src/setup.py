#!/home/leolio/.pyenv/shims/python3
from setuptools import setup
from Cython.Build import cythonize

setup(
  ext_modules=cythonize("src/StateLogic.pyx",compiler_directives={"language_level" : "3"})
)
