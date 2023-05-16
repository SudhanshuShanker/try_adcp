# setup.py
from setuptools import setup
from setuptools import find_namespace_packages

setup(
     name='CCSBLIB',
     scripts=[	'./bin_scripts/agfr',
          	'./bin_scripts/agfrgui',
		'./bin_scripts/pythonsh',
		'./bin_scripts/reduce_wwPDB_het_dict.txt'
              ], 
     data_files = [
                   ('lib',['./lib_files/libnlopt.so.0']),
                   ('bin',['./bin_scripts/autogrid4']),
                   ('bin',[ './bin_scripts/reduce']),
                   ],
     packages=find_namespace_packages(
        where='src',exclude='dist'),
     package_dir = {'': 'src'},
    # install_requires =["biopython>=1.76.0", "numpy>=1.18.0", "openbabel>=2.4.1","python >=3.6"],

)
