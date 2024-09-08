# setup.py

from setuptools import setup, find_packages

setup(
    name="crud_jt",
    version="0.1.0",
    description="A simple example library",
    author="Vlad Akymov",
    author_email="exwarvlad@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "msgpack",
        "cachetools"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
