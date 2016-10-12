'''
Created on 09. Okt. 2016

@author: chof
'''

from setuptools import setup

setup(name             = 'dbversions',
      version          = '0.7.1',
      author           = 'Eric PTAK',
      package_dir      = { '' : 'src' },
      packages = ['dbversions'],
      scripts=['src/dbconfig.py'] )