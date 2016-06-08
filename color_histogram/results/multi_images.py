# -*- coding: utf-8 -*-
# # @package color_histogram.results.multi_images
#
#  color_histogram.results.multi_images utility package.
#  @author      tody
#  @date        2016/06/08

import numpy as np
import matplotlib.pyplot as plt

from color_histogram.core.color_pixels import ColorPixels
from color_histogram.datasets.datasets import dataFile
from color_histogram.io_util.image import loadRGB
from color_histogram.results.results import batchResults, batchDataGroup
from color_histogram.plot.fig2np import figure2numpy
from color_histogram.results.hist_1d import histogram1DResult
from color_histogram.results.hist_2d import histogram2DResult
from color_histogram.results.hist_3d import histogram3DResult


# # Create multi-image pixels.
def createMultiImagePixels(data_name, data_ids):
    rgb_pixels = []

    num_cols = 3
    num_rows = (len(data_ids) + 2) / num_cols

    fig = plt.figure(figsize=(10, 7))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.1, hspace=0.1)

    font_size = 15
    plot_id = 1

    for data_id in data_ids:
        image_file = dataFile(data_name, data_id)
        image = loadRGB(image_file)

        rgb_pixels.extend(ColorPixels(image).rgb())

        fig.add_subplot(num_rows, num_cols, plot_id)
        plt.imshow(image)
        plt.axis('off')

        plot_id += 1

    rgb_pixels = np.array(rgb_pixels)
    multi_image = np.array(rgb_pixels).reshape(1, -1, 3)
    multi_tile = figure2numpy(fig)

    return multi_image, multi_tile


def hist1DMultiResultFunc(num_bins=32):
    def func(data_name, data_ids):
        multi_image, multi_tile = createMultiImagePixels(data_name, data_ids)
        histogram1DResult(data_name + "_multi", num_bins, multi_image, multi_tile)
    return func


# # Compute multi-image results for the given data names, ids.
def hist1DMultiResults(data_names, data_ids, num_bins=32):
    batchDataGroup(data_names, data_ids, hist1DMultiResultFunc(num_bins), "Histogram 1D(multi images)")


def hist2DMultiResultFunc(num_bins=32):
    def func(data_name, data_ids):
        multi_image, multi_tile = createMultiImagePixels(data_name, data_ids)
        histogram2DResult(data_name + "_multi", num_bins, multi_image, multi_tile)
    return func


# # Compute multi-image results for the given data names, ids.
def hist2DMultiResults(data_names, data_ids, num_bins=32):
    batchDataGroup(data_names, data_ids, hist2DMultiResultFunc(num_bins), "Histogram 2D(multi images)")


def hist3DMultiResultFunc(num_bins=32):
    def func(data_name, data_ids):
        multi_image, multi_tile = createMultiImagePixels(data_name, data_ids)
        histogram3DResult(data_name + "_multi", num_bins, multi_image, multi_tile)
    return func


# # Compute multi-image results for the given data names, ids.
def hist3DMultiResults(data_names, data_ids, num_bins=32):
    batchDataGroup(data_names, data_ids, hist3DMultiResultFunc(num_bins), "Histogram 3D(multi images)")

