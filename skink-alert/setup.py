from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='skink-alert',
      version=version,
      description="skink-alert is an app to monitor build status in skink",
      long_description="""\
skink-alert is a plugin that shows who broke the build in red or the status of all builds in a green screen""",
      classifiers=["Development Status :: 2 - Pre-Alpha",
				   "Intended Audience :: Developers",
				   "License :: OSI Approved",
				   "Natural Language :: English",
				   "Programming Language :: Python :: 2.5",], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Continuous Integration CI python',
      author='Bernardo Heynemann',
      author_email='heynemann@gmail.com',
      url='http://www.skinkci.org',
      license='OSI',
      packages=["skink-alert",],
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
