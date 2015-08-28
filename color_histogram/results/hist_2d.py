
# -*- coding: utf-8 -*-
## @package color_histogram.results.hist_2d
#
#  color_histogram.results.hist_2d utility package.
#  @author      tody
#  @date        2015/08/28

import os
import numpy as np
import matplotlib.pyplot as plt

from color_histogram.io_util.image import loadRGB
from color_histogram.cv.image import rgb, to32F

from color_histogram.datasets.google_image import dataFile
from color_histogram.results.results import resultFile
from color_histogram.plot.window import showMaximize
from color_histogram.core.hist_2d import Hist2D
from color_histogram.util.timer import timing_func


## Plot 2D color histograms for the target image, color space, channels.
@timing_func
def plotHistogram2D(C_32F, color_space, channels, ax):
    font_size = 15
    num_bins = 32

    plt.title("%s (%s, %s): %s bins" % (color_space,
                                        color_space[channels[0]],
                                        color_space[channels[1]],
                                        num_bins), fontsize=font_size)

    hist2D = Hist2D(C_32F, num_bins=num_bins, color_space=color_space, channels=channels)
    hist2D.plot(ax)


## Compute histogram 2D result for the image file.
def histogram2DResult(image_file):
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    fig_w = 10
    fig_h = 6
    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.95, wspace=0.4, hspace=0.2)

    font_size = 15
    fig.suptitle("Hisotogram 2D", fontsize=font_size)

    C_8U = loadRGB(image_file)

    h, w = C_8U.shape[:2]
    fig.add_subplot(231)
    plt.title("Original Image: %s x %s" % (w, h), fontsize=font_size)
    plt.imshow(C_8U)
    plt.axis('off')

    rgb_8U = rgb(C_8U)
    C_32F = to32F(rgb_8U)

    color_space = "hsv"
    channels_list = [[0, 1], [0, 2], [1,2]]

    plot_id = 234
    for channels in channels_list:
        ax = fig.add_subplot(plot_id)
        plotHistogram2D(C_32F, color_space, channels, ax)
        plot_id += 1

    result_name = image_name + "_hist2D"
    result_file = resultFile(result_name)
    plt.savefig(result_file, transparent=True)


## Compute histogram 2D results for the given data names, ids.
def histogram2DResults(data_names, data_ids):
    for data_name in data_names:
        print "Histogram 2D: %s" % data_name
        for data_id in data_ids:
            print "Data ID: %s" % data_id
            image_file = dataFile(data_name, data_id)
            histogram2DResult(image_file)

if __name__ == '__main__':
    data_names = ["flower"]
    data_ids = [0, 1, 2]

    histogram2DResults(data_names, data_ids)