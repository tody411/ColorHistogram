# -*- coding: utf-8 -*-
## @package color_histogram.core.hist_2d
#
#  Implementation of 2D color histograms.
#  @author      tody
#  @date        2015/08/28

import numpy as np

from color_histogram.core.color_pixels import ColorPixels


## Implementation of 2D color histograms.
class Hist2D:
    ## Constructor
    #  @param image          input image.
    #  @param num_bins       target number of histogram bins.
    #  @param alpha          low density clip.
    #  @param color_space    target color space.
    #  @param channels       target color channels.
    def __init__(self, image, num_bins=16, alpha=0.1, color_space='rgb', channels=[0, 1]):
        self._computeTargetPixels(image, color_space, channels)
        self._num_bins = num_bins
        self._alpha = alpha
        self._color_space = color_space
        self._channels = channels

        self._computeColorRange()
        self._computeHistogram()

        self._plotter = Hist2DPlot(self)

    def colorSpace(self):
        return self._color_space

    def channels(self):
        return self._channels

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

    def _computeTargetPixels(self, image, color_space, channels):
        color_pixels = ColorPixels(image)
        self._pixels = color_pixels.pixels(color_space)[:, channels]
        self._rgb_pixels = color_pixels.rgb()

    def _computeColorRange(self):
        pixels = self._pixels
        cs = pixels.shape[1]

        c_min = np.zeros(cs)
        c_max = np.zeros(cs)
        for ci in xrange(cs):
            c_min[ci] = np.min(pixels[:, ci])
            c_max[ci] = np.max(pixels[:, ci])

        self._color_range = [c_min, c_max]

    def _computeHistogram(self):
        pixels = self._pixels
        num_bins = self._num_bins
        c_min, c_max = self._color_range

        hist_bins = np.zeros((num_bins, num_bins), dtype=np.float32)
        color_bins = np.zeros((num_bins, num_bins, 3), dtype=np.float32)

        color_ids = (num_bins - 1) * (pixels - c_min) / (c_max - c_min)
        color_ids = np.int32(color_ids)

        for pi, color_id in enumerate(color_ids):
            hist_bins[color_id[0], color_id[1]] += 1
            color_bins[color_id[0], color_id[1]] += self._rgb_pixels[pi]

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


class Hist2DPlot:

    def __init__(self, hist2D, density_size_range=[10, 100]):
        self._hist2D = hist2D

    def plot(self, ax, density_size_range=[10, 100]):
        color_samples = self._hist2D.colorCoordinates()
        density_sizes = self._densitySizes(density_size_range)
        colors = self._hist2D.rgbColors()

        ax.scatter(color_samples[:, 0], color_samples[:, 1], color=colors, s=density_sizes)
        self._axisSetting(ax)

    def _range2ticks(self, xrange, yrange):
        xticks = np.linspace(xrange[0], xrange[1], 4)
        xticks = np.around(xticks, decimals=1)
        xticks[xticks>10] = np.rint(xticks[xticks>10])
        yticks = np.linspace(yrange[0], yrange[1], 4)
        yticks = np.around(yticks, decimals=1)
        yticks[yticks>10] = np.rint(yticks[yticks>10])

        return xticks, yticks

    def _range2lims(self, xrange, yrange):
        xunit = 0.1 * (xrange[1] - xrange[0])
        yunit = 0.1 * (yrange[1] - yrange[0])

        xlim = np.array(xrange)
        xlim[0] += -xunit
        xlim[1] += xunit

        ylim = np.array(yrange)
        ylim[0] += -yunit
        ylim[1] += yunit

        return xlim, ylim

    def _densitySizes(self, density_size_range):
        color_densities = self._hist2D.colorDensities()

        density_size_min, density_size_max = density_size_range
        density_size_factor = density_size_max / density_size_min
        density_sizes = density_size_min * np.power(density_size_factor, color_densities)
        return density_sizes

    def _axisSetting(self, ax):
        color_space = self._hist2D.colorSpace()
        channels = self._hist2D.channels()

        ax.set_xlabel(color_space[channels[0]])
        ax.set_ylabel(color_space[channels[1]], rotation='horizontal')

        color_range = self._hist2D.colorRange()
        tick_range = np.array(color_range).T
        xrange = tick_range[0]
        yrange = tick_range[1]

        xticks, yticks = self._range2ticks(xrange, yrange)

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        xlim, ylim = self._range2lims(xrange, yrange)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
