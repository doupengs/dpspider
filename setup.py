#!/usr/bin/env python
#coding:utf-8

from setuptools import setup,find_packages

setup(
      name="dpspider",
      version="2.0.1",
      description="A lightweight Web Crawling and Web Scraping framework.(v2.x.x add distributed processing)",
      author="doupeng",
      author_email = 'doupeng1993@sina.com',
      url="https://github.com/doupengs/dpspider",
      license="GPL",
      packages= find_packages(),
      install_requires=[
          'requests>=2.10',
          'lxml>=3.6',
          'MySQL-python>=1.2.3',
          'redis>=2.10'
          ]
      )
