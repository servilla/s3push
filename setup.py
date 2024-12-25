#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: setup.py

:Synopsis:

:Author:
    servilla

:Created:
    2023-01-21
"""
from os import path
from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "LICENSE"), encoding="utf-8") as f:
    full_license = f.read()

with open(path.join(here, "./src/s3push/VERSION.txt"), encoding="utf-8") as f:
    version = f.read()


setup(
    name='s3push',
    version=version,
    description='PASTA to S3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mark Servilla",
    url="https://github.com/servilla/s3push",
    license=full_license,
    packages=find_packages(where="src", include=["s3push"]),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=" >= 3.13",
    install_requires=[
        "boto3 >=1.35.82,<2",
        "click >=8.1.7,<9",
        "daiquiri >=3.0.0,<4",
        "sqlalchemy >=2.0.36,<3",
        "ruff >=0.8.3,<0.9",
        "pytest >=8.3.4,<9",
        "psycopg2 >=2.9.9,<3",
        "pip >=24.3.1,<25",
        "setuptools >=75.6.0,<76",
    ],
    entry_points={"console_scripts": ["push=s3push.push:push"]},
    classifiers=["License :: OSI Approved :: Apache Software License",],
)


def main():
    return 0


if __name__ == "__main__":
    main()
