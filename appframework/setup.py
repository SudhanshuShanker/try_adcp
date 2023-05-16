# setup.py
from setuptools import setup
from setuptools import find_namespace_packages

setup(
     name='AppFramework',
     packages=find_namespace_packages(
        where='src',exclude='dist'),
     package_dir = {'': 'src'},
    # install_requires =["biopython>=1.76.0", "numpy>=1.18.0", "openbabel>=2.4.1","python >=3.6"],

)
