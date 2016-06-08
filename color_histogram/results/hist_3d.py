# -*- coding: utf-8 -*-
# # @package color_histogram.results.hist_3d
#
#  cCompute 3D color histogram result.
#  @author      tody
#  @date        2015/08/28

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from color_histogram.io_util.image import loadRGB
from color_histogram.cv.image import rgb, to32F, rgb2Lab, rgb2hsv
from color_histogram.core.hist_3d import Hist3D
from color_histogram.datasets.datasets import dataFile
from color_histogram.results.results import resultFile, batchResults
from color_histogram.plot.window import showMaximize
from color_histogram.util.timer import timing_func


# # Plot 3D color histograms for the target image, color space, channels.
@timing_func
def plotHistogram3D(image, num_bins, color_space, ax):
    font_size = 15
    plt.title("%s: %s bins" % (color_space, num_bins), fontsize=font_size)

    hist3D = Hist3D(image, num_bins=num_bins, color_space=color_space)
    hist3D.plot(ax)


# # Create histogram 3D result function.
def histogram3DResultFunc(num_bins=32):
    def func(image_file):
        histogram3DResult(image_file, num_bins)
    return func


# # Compute histogram 3D result for the image file.
def histogram3DResult(image_file, num_bins=32, image=None, tile=None):
    image_name = os.path.basename(image_file)
    if image is None:
        image_name = os.path.basename(image_file)
        image_name = os.path.splitext(image_name)[0]
        image = loadRGB(image_file)

    if tile is None:
        tile = image

    fig_w = 10
    fig_h = 6
    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.02, hspace=0.2)

    font_size = 15
    fig.suptitle("Hisotogram 3D", fontsize=font_size)

    h, w = image.shape[:2]
    fig.add_subplot(231)
    plt.title("Original Image: %s x %s" % (w, h), fontsize=font_size)
    plt.imshow(tile)
    plt.axis('off')

    color_spaces = ["rgb", "Lab", "hsv"]

    plot_id = 234
    for color_space in color_spaces:
        ax = fig.add_subplot(plot_id, projection='3d')
        plotHistogram3D(image, num_bins, color_space, ax)
        plot_id += 1

    result_name = image_name + "_hist3D"
    result_file = resultFile(result_name)
    plt.savefig(result_file, transparent=True)


# # Compute histogram 3D results for the data names, ids.
def histogram3DResults(data_names, data_ids, num_bins=32):
    batchResults(data_names, data_ids, histogram3DResultFunc(num_bins), "Histogram 3D")

if __name__ == '__main__':
    data_names = ["flower"]
    data_ids = [0, 1, 2]

    histogram3DResults(data_names, data_ids)
