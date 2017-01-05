#!/usr/bin/env python
from setuptools import setup
import plucky

setup(
    name=plucky.__name__,
    version=plucky.__version__,
    description=plucky.__doc__.strip(),
    long_description=open('README.rst').read(),
    author=plucky.__author__,
    author_email=plucky.__author_email__,
    url=plucky.__url__,
    license=plucky.__license__,
    packages=[plucky.__name__],
    package_dir={plucky.__name__: plucky.__name__},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='pluck itemgetter safe nested get'
)
