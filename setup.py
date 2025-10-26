# setup.py

from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "NET_MARKDOWN_README.md").read_text()

setup(
    name="crudjt",
    version="1.0.0.beta.0",
    description="Simlifies user session. Login / Logout / Authorization",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Vlad Akymov",
    author_email="support@crudjt.com",
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
