#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='SMT Corpus Toolkit',
      version='0.1',
      description='SMT Corpus Toolkit',
      author='Leo Jiang',
      author_email='leo.jiang.dev@gmail.com',
      packages=['corpustoolkit'],
      scripts=['scripts/corpustk',
               'scripts/tmx2bitext'
               ],
      license='FreeBSD License'
     )
