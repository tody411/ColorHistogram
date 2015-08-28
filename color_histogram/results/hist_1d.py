# -*- coding: utf-8 -*-
## @package color_histogram.results.hist_1d
#
#  Compute 1D color histogram result.
#  @author      tody
#  @date        2015/08/28

import os
import numpy as np
import matplotlib.pyplot as plt

from color_histogram.io_util.image import loadRGB
from color_histogram.cv.image import rgb, to32F

from color_histogram.datasets.google_image import dataFile
from color_histogram.results.results import resultFile, batchResults
from color_histogram.plot.window import showMaximize
from color_histogram.util.timer import timing_func
from color_histogram.core.hist_1d import Hist1D


## Plot 1D color histograms for the target image, color space, channels.
@timing_func
def plotHistogram1D(C_32F, color_space, channel, ax):
    font_size = 15
    num_bins = 32

    plt.title("%s (%s): %s bins" % (color_space,
                                        color_space[channel],
                                        num_bins), fontsize=font_size)

    hist1D = Hist1D(C_32F, num_bins=num_bins, color_space=color_space, channel=channel)
    hist1D.plot(ax)


## Compute histogram 1D result for the image file.
def histogram1DResult(image_file):
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    fig_w = 10
    fig_h = 6
    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.95, wspace=0.3, hspace=0.2)

    font_size = 15
    fig.suptitle("Hisotogram 1D", fontsize=font_size)

    C_8U = loadRGB(image_file)

    h, w = C_8U.shape[:2]
    fig.add_subplot(231)
    plt.title("Original Image: %s x %s" % (w, h), fontsize=font_size)
    plt.imshow(C_8U)
    plt.axis('off')

    rgb_8U = rgb(C_8U)
    C_32F = to32F(rgb_8U)

    color_targets = [["Lab", 0], ["hsv", 0], ["hsv", 2]]

    plot_id = 234
    for color_target in color_targets:
        ax = fig.add_subplot(plot_id)
        color_space, channel = color_target
        plotHistogram1D(C_32F, color_space, channel, ax)
        plot_id += 1

    result_name = image_name + "_hist1D"
    result_file = resultFile(result_name)
    plt.savefig(result_file, transparent=True)


## Compute histogram 1D results for the given data names, ids.
def histogram1DResults(data_names, data_ids):
    batchResults(data_names, data_ids, histogram1DResult, "Histogram 1D")


if __name__ == '__main__':
    data_names = ["flower"]
    data_ids = [0, 1, 2]

    histogram1DResults(data_names, data_ids)