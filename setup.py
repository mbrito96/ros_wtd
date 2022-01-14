#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup(
    packages=['wtd_ros', 'wtd_ros.actions', 'wtd_ros.monitors'],
    package_dir={'': 'include'},
)

setup(**setup_args)