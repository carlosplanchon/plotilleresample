#!/usr/bin/env python3

from setuptools import setup


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="plotilleresample",
    packages=["plotilleresample"],
    version="0.2",
    license="GPL3",
    description="Python3 module to resample datasets"
            "before plotting with Plotille.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/plotilleresample",
    download_url="https://github.com/carlosplanchon/"
        "plotilleresample/archive/v0.2.tar.gz",
    keywords=["plotting", "ascii", "math", "resample"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
