import os
from setuptools import setup, find_packages, Extension
import numpy as np
from sysconfig import get_paths


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="nisip",
    version="0.0.2",
    url="https://github.com/AndreiZoltan/sandpile",
    author="Andrei Zoltan",
    license="GPLv2",
    packages=find_packages(exclude=["tests", "docs"]),
    description="A Python package for sandpile models.",
    long_description_content_type="text/markdown",
    long_description=read("README.md"),
    ext_modules=[Extension("relax", sources=["cnisip/relax.c"],
                           include_dirs=[np.get_include(), get_paths()["include"]],
                           extra_compile_args = ["-O3", "-march=native"])],
    classifiers=[],
)
