# -*- coding: utf-8 -*-
"""
    Setup file for ortscraper.

"""
import sys

from pkg_resources import require, VersionConflict
from setuptools import setup, find_packages

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

if __name__ == "__main__":
    setup(name='KEGGScraper',
          version='0.01',
          description='Tool to collect information in bulk from KEGG BRITE Database',
          licence="MIT",
          long_description=long_description,
          author='Marta Lopes Gomes',
          author_email='martalopesgomes@hotmail.com',
          url='',
          # Commands
          scripts=['src/MultipleRequests.py', 'src/aux.py'],
          # classifiers=[],
          packages=find_packages(),
          # py_modules=[],
          install_requires=required,
          entry_points={
              'console_scripts':
                  ['download_kos=src.download_kos:run'],
          },
          # Data - see this better
          # package_data=[]
          )
