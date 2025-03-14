from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='statelogic',
    version='1.0.1',  
    description='A library for state management with colored messages',
    author='Wong Chun Fai',
    author_email='wilgat.wong@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Wilgat/Statelogic',  
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)