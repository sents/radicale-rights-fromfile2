#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="radicale-rights-fromfile2",
    version="0.1",
    description="""
    A radicale plugin to use the from_file rights class plus
    displayname matching""",
    long_description="""
This is a radicale rights plugin enabling the use of multiple rights plugins.
Access is granted whenever one of the specified plugins grant access.
For more information read the README.md.
    """,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    license="GNU GPLv3",
    install_requires=["radicale"],
    author="Finn Krein",
    author_email="finn@krein.moe",
    url="https://github.com/sents/radicale_rights_fromfile2",
    packages=["radicale_rights_fromfile2"],
)
