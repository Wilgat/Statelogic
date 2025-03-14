#!/bin/bash
find . -type d -name __pycache__ -exec rm -rf {} \;
find . -type d -name __pycache__ -exec rm -rf {} \;
find . -type d -name statelogic.egg-info -exec rm -rf {} \;
find . -type f -name "._*" -exec rm -rf {} \;
find . -type f -name "._*" -exec rm -rf {} \;
rm -rf build
rm -rf dist
python3 setup.py sdist bdist_wheel