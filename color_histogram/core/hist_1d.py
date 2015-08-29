
# -*- coding: utf-8 -*-
## @package color_histogram.core.hist_1d
#
#  Implementation of 1D color histograms.
#  @author      tody
#  @date        2015/08/29

import numpy as np

from color_histogram.core.color_pixels import ColorPixels


## Implementation of 2D color histograms.
class Hist1D:
    ## Constructor
    #  @param image          input image.
    #  @param num_bins       target number of histogram bins.
    #  @param alpha          low density clip.
    #  @param color_space    target color space.
    #  @param channels       target color channels.
    def __init__(self, image, num_bins=16, alpha=0.1, color_space='Lab', channel=0):
        self._computeTargetPixels(image, color_space, channel)
        self._num_bins = num_bins
        self._alpha = alpha
        self._color_space = color_space
        self._channel = channel

        self._computeColorRange()
        self._computeHistogram()

        self._plotter = Hist1DPlot(self)

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
        color_ids = np.array(color_ids).T

        num_bins = self._num_bins
        c_min, c_max = self._color_range
        color_samples = c_min + (color_ids * (c_max - c_min)) / float(num_bins - 1.0)

        return color_samples

    def colorDensities(self):
        color_densities = np.float32(self._hist_bins[self._histPositive()])

        density_max = np.max(color_densities)
        color_densities = color_densities / density_max

        return color_densities

    def rgbColors(self):
        colors = self._color_bins[self._histPositive(), :]
        colors = np.clip(colors, 0.0, 1.0)
        return colors

    def colorRange(self):
        return self._color_range

    def plot(self, ax, density_size_range=[10, 100]):
        self._plotter.plot(ax, density_size_range)

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

        color_ids = (num_bins - 1) * (pixels - c_min) / (c_max - c_min)

        color_ids = np.int32(color_ids)

        for pi, color_id in enumerate(color_ids):
            hist_bins[color_id] += 1
            color_bins[color_id] += self._rgb_pixels[pi]

        self._hist_bins = hist_bins

        hist_positive = self._hist_bins > 0.0

        for ci in xrange(3):
            color_bins[hist_positive, ci] /= self._hist_bins[hist_positive]

        self._color_bins = color_bins

        self._clipLowDensity()

    def _clipLowDensity(self):
        density_mean = np.mean(self._hist_bins)
        low_density = self._hist_bins < density_mean * self._alpha
        self._hist_bins[low_density] = 0.0

        for ci in xrange(3):
            self._color_bins[low_density, ci] = 0.0

    def _histPositive(self):
        return self._hist_bins > 0.0


class Hist1DPlot:

    def __init__(self, hist1D, density_size_range=[10, 100]):
        self._hist1D = hist1D

    def plot(self, ax, density_size_range=[10, 100]):
        color_samples = self._hist1D.colorCoordinates()
        color_densities = self._hist1D.colorDensities()

        colors = self._hist1D.rgbColors()

        color_range = self._hist1D.colorRange()
        width = (color_range[1] - color_range[0]) / float(self._hist1D.numBins())

        ax.bar(color_samples, color_densities, width=width, color=colors)
        self._axisSetting(ax)

    def _range2ticks(self, tick_range):
        ticks = np.around(tick_range, decimals=1)
        ticks[ticks > 10] = np.rint(ticks[ticks > 10])
        return ticks[0], ticks[1]

    def _range2lims(self, tick_range):
        unit = 0.1 * (tick_range[:, 1] - tick_range[:, 0])
        lim = np.array(tick_range)
        lim[1, 1] += unit[1]

        return lim[0], lim[1]

    def _densitySizes(self, density_size_range):
        color_densities = self._hist2D.colorDensities()

        density_size_min, density_size_max = density_size_range
        density_size_factor = density_size_max / density_size_min
        density_sizes = density_size_min * np.power(density_size_factor, color_densities)
        return density_sizes

    def _axisSetting(self, ax):
        color_space = self._hist1D.colorSpace()
        channel = self._hist1D.channel()

        ax.set_xlabel(color_space[channel])
        ax.set_ylabel("Density")

        color_range = self._hist1D.colorRange()
        tick_range = np.array([color_range, [0.0, 1.0]])
        xticks, yticks = self._range2ticks(tick_range)

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        xlim, ylim = self._range2lims(tick_range)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)