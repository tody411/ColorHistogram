# -*- coding: utf-8 -*-
# # @package color_histogram.examples.hist_3d
#
#  Minimal example of 3D color histograms.
#  @author      tody
#  @date        2015/08/29

from color_histogram.io_util.image import loadRGB
from color_histogram.core.hist_3d import Hist3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from color_histogram.datasets.datasets import dataFile

image_file = dataFile("flower", 0)

# Load image.
image = loadRGB(image_file)

# 16 bins, rgb color space
hist3D = Hist3D(image, num_bins=16, color_space='rgb')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
hist3D.plot(ax)
plt.show()
