# -*- coding: utf-8 -*-
# # @package color_histogram.examples.hist_2d
#
#  Minimal example of 2D color histograms.
#  @author      tody
#  @date        2015/08/29

from color_histogram.io_util.image import loadRGB
from color_histogram.core.hist_2d import Hist2D
import matplotlib.pyplot as plt

from color_histogram.datasets.datasets import dataFile

image_file = dataFile("flower", 0)

# Load image.
image = loadRGB(image_file)

# 32 bins, hsv color space, target channels (h, s) ('hsv'[0], 'hsv'[1])
hist2D = Hist2D(image, num_bins=32, color_space='hsv', channels=[0, 1])

fig = plt.figure()
ax = fig.add_subplot(111)
hist2D.plot(ax)
plt.show()
