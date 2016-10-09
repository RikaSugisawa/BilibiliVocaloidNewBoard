#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pybvb',
    packages=find_packages(exclude=['test*']),
    version=open('VERSION').read().strip(),
    include_package_data=True,
    ext_modules=[],
    zip_safe=False,
    author='RikaSugisawa, TEOA',
    author_email='tjj.rikap@gmail.com, cruiser0631@gmail.com',
    description='Automated original Vocaloid ranker in Python.',
    keywords=['Bilibili', 'Vocaloid', 'ranking'],
    url='https://github.com/RikaSugisawa/BilibiliVocaloidNewBoard.git',
    download_url='https://github.com/RikaSugisawa/BilibiliVocaloidNewBoard.git',
    license='Apache-2.0',
    platforms='Any',
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Entertainment',
        'Intended Audience :: Statistics',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese, English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',]
)
