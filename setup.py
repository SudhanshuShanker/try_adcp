# setup.py
from setuptools import setup
from setuptools import find_namespace_packages

setup(
     name='ADCP',
     scripts=['bin_scripts/adcp'], 
     data_files = [('bin',['./bin_scripts/adcp_Linux-x86_64_1.1']),
                   ('lib',['./lib_files/libnlopt.so.0']),
                   ],
     packages=find_namespace_packages(
        where='src',exclude='dist'),
     package_dir = {'': 'src'},
    # install_requires =['pybel==0.15.0', 'biopython==1.76','colorama','numpy==1.18.5'],


)
