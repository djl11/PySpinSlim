from distutils.core import setup
import setuptools

setup(name='PySpinSlim',
      version='1.0',
      description='Thin wrapper around PySpin, for interfacing with FLIR cameras using Spinnaker',
      author='Daniel Lenton',
      author_email='djl11@ic.ac.uk',
      packages=setuptools.find_packages(),
      )