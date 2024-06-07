#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : setup.py
# Author             : QU35T-code (Exegol)
# Date created       : 07 jun 2024

import setuptools

VERSION = "1.0.0"

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [x.strip() for x in f.readlines()]

setuptools.setup(
    name="exegolx",
    version=VERSION,
    description="Exegolx is a tweeter bot.",
    url="https://github.com/QU35T-code/exegolx",
    author="QU35T-code",
    license="GPL3",
    package_data={'exegolx': ['exegolx/']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'exegolx=exegolx.exegolx:main'
        ]
    }
)
