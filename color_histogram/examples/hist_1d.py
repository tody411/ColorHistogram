# -*- coding: utf-8 -*-
# # @package color_histogram.examples.hist_1d
#
#  Minimal example of 1D color histograms.
#  @author      tody
#  @date        2015/08/29

from color_histogram.io_util.image import loadRGB
from color_histogram.core.hist_1d import Hist1D
import matplotlib.pyplot as plt

from color_histogram.datasets.datasets import dataFile

image_file = dataFile("flower", 0)

# Load image.
image = loadRGB(image_file)

# 16 bins, Lab color space, target channel L ('Lab'[0])
hist1D = Hist1D(image, num_bins=16, color_space='Lab', channel=0)

fig = plt.figure()
ax = fig.add_subplot(111)
hist1D.plot(ax)
plt.show()
