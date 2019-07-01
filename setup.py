#!/usr/bin/env python
from setuptools import setup


setup(
    name="pylibra",
    version="0.0.1",
    author="Band Protocol",
    author_email="opensource@bandprotocol.com",
    description="A Python client for Libra network",
    url="https://github.com/bandprotocol/pylibra",
    packages=["pylibra"],
    zip_safe=False,
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ],
)
