
# -*- coding: utf-8 -*-
## @package color_histogram.core.hist_1d
#
#  Implementation of 1D color histograms.
#  @author      tody
#  @date        2015/08/29

import numpy as np

from color_histogram.core.color_pixels import ColorPixels
from color_histogram.core.hist_common import colorCoordinates, colorDensities, rgbColors, clipLowDensity, range2ticks


## Implementation of 1D color histograms.
class Hist1D:
    ## Constructor
    #  @param image          input image.
    #  @param num_bins       target number of histogram bins.
    #  @param alpha          low density clip.
    #  @param color_space    target color space. 'rgb' or 'Lab' or 'hsv'.
    #  @param channel        target color channel. 0 with 'Lab' = L channel.
    def __init__(self, image, num_bins=16, alpha=0.1, color_space='Lab', channel=0):
        self._computeTargetPixels(image, color_space, channel)
        self._num_bins = num_bins
        self._alpha = alpha
        self._color_space = color_space
        self._channel = channel

        self._computeColorRange()
        self._computeHistogram()

        self._plotter = Hist1DPlot(self)

    ## Plot histogram.
    def plot(self, ax):
        self._plotter.plot(ax)

    def numBins(self):
        return self._num_bins

    def colorSpace(self):
        return self._color_space

    def channel(self):
        return self._channel

    def colorIDs(self):
        color_ids = np.where(self._histPositive())
        return color_ids

    def colorCoordinates(self):
        color_ids = self.colorIDs()
        num_bins = self._num_bins
        color_range = self._color_range
        return colorCoordinates(color_ids, num_bins, color_range)

    def colorDensities(self):
        return colorDensities(self._hist_bins)

    def rgbColors(self):
        return rgbColors(self._hist_bins, self._color_bins)

    def colorRange(self):
        return self._color_range

    def _computeTargetPixels(self, image, color_space, channel):
        color_pixels = ColorPixels(image)
        self._pixels = color_pixels.pixels(color_space)[:, channel]
        self._rgb_pixels = color_pixels.rgb()

    def _computeColorRange(self):
        pixels = self._pixels
        c_min = np.min(pixels)
        c_max = np.max(pixels)

        self._color_range = [c_min, c_max]

    def _computeHistogram(self):
        pixels = self._pixels

        num_bins = self._num_bins
        c_min, c_max = self._color_range

        hist_bins = np.zeros((num_bins), dtype=np.float32)
        color_bins = np.zeros((num_bins, 3), dtype=np.float32)

        color_ids = (num_bins - 1) * (pixels - c_min) // (c_max - c_min)

        color_ids = np.int32(color_ids)

        for pi, color_id in enumerate(color_ids):
            hist_bins[color_id] += 1
            color_bins[color_id] += self._rgb_pixels[pi]

        self._hist_bins = hist_bins

        hist_positive = self._hist_bins > 0.0

        for ci in range(3):
            color_bins[hist_positive, ci] /= self._hist_bins[hist_positive]

        self._color_bins = color_bins

        self._clipLowDensity()

    def _clipLowDensity(self):
        clipLowDensity(self._hist_bins, self._color_bins, self._alpha)

    def _histPositive(self):
        return self._hist_bins > 0.0


## 1D color histogram plotter.
class Hist1DPlot:
    ## Constructor.
    #  @param hist1D histogram for plotting.
    def __init__(self, hist1D):
        self._hist1D = hist1D

    def plot(self, ax):
        color_samples = self._hist1D.colorCoordinates()
        color_densities = self._hist1D.colorDensities()

        colors = self._hist1D.rgbColors()

        color_range = self._hist1D.colorRange()
        width = (color_range[1] - color_range[0]) / float(self._hist1D.numBins())

        ax.bar(color_samples, color_densities, width=width, color=colors)
        self._axisSetting(ax)

    def _range2lims(self, tick_range):
        unit = 0.1 * (tick_range[:, 1] - tick_range[:, 0])
        lim = np.array(tick_range)
        lim[0, 0] += -unit[0]
        lim[0, 1] += unit[0]
        lim[1, 1] += unit[1]

        return lim[0], lim[1]

    def _axisSetting(self, ax):
        color_space = self._hist1D.colorSpace()
        channel = self._hist1D.channel()

        ax.set_xlabel(color_space[channel])
        ax.set_ylabel("Density")

        color_range = self._hist1D.colorRange()
        tick_range = np.array([color_range, [0.0, 1.0]])
        xticks, yticks = range2ticks(tick_range)

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        xlim, ylim = self._range2lims(tick_range)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)