import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='nisip',
    version='0.0.1',
    url='https://github.com/AndreiZoltan/sandpile',
    author='Andrei Zoltan',
    license='GPLv2',
    packages=find_packages(exclude=['tests', 'docs']),
    description='A Python package for sandpile models.',
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
)