# -*- coding: utf-8 -*-
## @package setup
#
#  setup utility package.
#  @author      tody
#  @date        2015/08/14

from setuptools import setup, find_packages
from color_histogram import __author__, __version__, __license__

setup(
        name = 'color_histogram',
        version = __version__,
        description = 'Simple python demos of Color Histogram.',
        license = __license__,
        author = __author__,
        url = 'https://github.com/tody411/ColorHistogram.git',
        packages = find_packages(),
        install_requires = ['docopt'],
        )

