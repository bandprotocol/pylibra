import os
from setuptools import setup


REQUIREMENTS = [
    line.strip()
    for line in open(os.path.join(os.path.dirname(__file__), "requirements.txt")).readlines()
]


setup(
    name="pylibra",
    version="0.0.3",
    license="MIT",
    author="Band Protocol",
    author_email="opensource@bandprotocol.com",
    description="A Python client for Libra network",
    url="https://github.com/bandprotocol/pylibra",
    packages=["pylibra"],
    keywords=["libra", "client", "cryptocurrency", "blockchain"],
    install_requires=REQUIREMENTS,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ],
)
