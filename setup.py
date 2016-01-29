from distutils.core import setup

setup(
    name="meniga_client",
    packages=["meniga_client"],
    version="0.9.0",
    description="Client for the Meniga API",
    author="Dagur Ammendrup",
    author_email="dagurp@gmail.com",
    url="https://github.com/Dagur/meniga_client",
    keywords=["meniga", "api"],
    requires=['requests'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    long_description="""\
Meniga API Client
-------------------------------------
A python library for interfacing with the Meniga APIs (which are not publicly available).

This is a port of https://github.com/krummi/meniga_client

Look there for more information before using this.

Requires Python 3
"""
)
