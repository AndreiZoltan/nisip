import os
from setuptools import setup, find_packages, Extension
from sysconfig import get_paths
from pathlib import Path
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

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
    ext_modules=[Extension("cnisip", sources=["cnisip/cnisip.c"],
                           include_dirs=[np.get_include(), get_paths()["include"],
                           f"{dir_path}/cnisip/"],
                           extra_compile_args = ["-O3", "-march=native"])],
    classifiers=[],
)
