#!/usr/bin/env python

from setuptools import setup

setup(
    name='py-brotherlabel',
    version='0.1.0',
    description='Raster print package for Brother label printers',
    author='Masato Mizuta',
    author_email='mst.mizuta@gmail.com',
    url='https://github.com/masatomizuta/py-brotherlabel/',
    packages=['brotherlabel', 'brotherlabel.backends'],
    install_requires=[
        'Pillow',
        'pyusb'
    ],
    keywords='Brother PT-P950NW'
)
