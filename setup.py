from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="crudjt",
    version="1.0.0b3",
    description="Fast B-tree–backed token store for stateful sessions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Vlad Akymov (v_akymov)",
    author_email="support@crudjt.com",
    url="https://github.com/crudjt/crudjt-python",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "msgpack>=1.0,<2",
        "cachetools>=5,<6",
        "grpcio>=1.60,<2",
        "protobuf>=6.0,<7.0"
    ],
    project_urls={
        "Documentation": "https://github.com/crudjt/crudjt-python#readme",
        "Source": "https://github.com/crudjt/crudjt-python",
        "Tracker": "https://github.com/crudjt/crudjt-python/issues",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    keywords="token, session, authentication, authorization",
    python_requires='>=3.8',
)
