# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="statelogic",
    version="1.2.1",
    description="A safe, pure-Python finite state machine with colored terminal logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Wong Chun Fai",
    author_email="wilgat.wong@gmail.com",
    url="https://github.com/Wilgat/Statelogic",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        # Universal support
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",

        # General metadata
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable",
        "Typing :: Typed",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    license="MIT",
    keywords="fsm state-machine statelogic logging colored terminal safe-state python2 python3",
    project_urls={
        "Bug Tracker": "https://github.com/Wilgat/Statelogic/issues",
        "Source Code": "https://github.com/Wilgat/Statelogic",
        "Changelog": "https://github.com/Wilgat/Statelogic/blob/main/CHANGELOG.md",
    },
)