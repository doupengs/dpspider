#!/usr/bin/env python
#coding:utf-8

from setuptools import setup,find_packages
from dpspider import __version__


setup(
    name="dpspider",
    version=__version__,
    description="A Web Crawling and Web Scraping framework.",
    author="doupeng",
    author_email = 'doupeng1993@sina.com',
    url="https://github.com/doupengs/dpspider",
    license="GPL",
    packages= find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Web Scraping Development :: Python Modules',
        'License :: GPL License',
        'Programming Language :: Python :: 2.7',
        ],
    install_requires=[
        'requests>=2.10',
        'lxml>=3.6',
        'MySQL-python>=1.2.3',
        'redis>=2.10'
      ]
    )
