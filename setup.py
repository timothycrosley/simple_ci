#!/usr/bin/env python

import subprocess
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup, Command

setup(name='simple_ci',
      version='0.0.1',
      description='Simple CI may quite possibly be the most simplistic ci server ever created.',
      author='Timothy Crosley',
      author_email='timothy.crosley@gmail.com',
      url='https://github.com/timothycrosley/simple_ci',
      license="MIT",
      py_modules=['simple_ci'],
      entry_points={
        'console_scripts': [
            'ci_worker = simple_ci:worker.cli',
        ]
      },
      requires=['hug', 'hot_redis', 'sh', 'Pillow'],
      install_requires=['hug', 'hot_redis', 'sh', 'Pillow'],
      keywords='Todo, Python, Python3',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Utilities'])
