import io
import os
from setuptools import setup


README = io.open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8").read()
REQUIREMENTS = [
    line.strip()
    for line in io.open(os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8").readlines()
]


setup(
    name="pylibra",
    version="0.1.9",
    license="MIT",
    author="Band Protocol",
    author_email="opensource@bandprotocol.com",
    description="A Python client for Libra network",
    long_description=README,
    long_description_content_type='text/markdown',
    url="https://github.com/bandprotocol/pylibra",
    packages=["pylibra", "pylibra.wallet", "pylibra.proto", "pylibra.transaction"],
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
