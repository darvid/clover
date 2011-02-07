#!/usr/bin/env python2
"""
    clover
    ~~~~~~

    A simplistic COLOURlovers interface.
"""
from setuptools import setup, find_packages
from clover import __version__


setup(
    name="clover",
    version=__version__,
    license="BSD",
    description=__doc__,
    packages=["clover"],
    namespace_packages=["clover"]
)
