# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
  name="sio2puppetMaster",
  version="0.1",
  packages=find_packages(),
  install_requires=[],
  scripts=['scripts/sio2pm-spawndocker'],
  license="MIT",
  author="Mateusz Żółtak",
  author_email="zozlak@zozlak.org"
)

