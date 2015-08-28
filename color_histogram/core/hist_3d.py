
# -*- coding: utf-8 -*-
## @package color_histogram.core.hist_3d
#
#  Implementation of 3D color histograms.
#  @author      tody
#  @date        2015/08/28

import numpy as np

from color_histogram.cv.image import to32F, rgb, hsv2rgb, Lab2rgb


## Implementation of 3D color histograms.
class Hist3D:
    ## Constructor
    #  @param image          input image.
    #  @param num_bins       target number of histogram bins.
    #  @param alpha          low density clip.
    def __init__(self, image,
                 num_bins=16, alpha=0.1, color_space="rgb",
                 density_size_range=[10, 100]):
        self.pixels = self.toPixels(image)
        self._num_bins = num_bins
        self._alpha = alpha
        self._color_space = color_space
        self._density_size_range = density_size_range

        self._computeColorRange()
        self._computeHistogram()

    def toPixels(self, image):
        if len(image.shape) == 2:
            h, w = image.shape
            return image.reshape((h * w))

        h, w, cs = image.shape
        return image.reshape((-1, cs))

    def _computeColorRange(self):
        pixels = self.pixels

        cs = pixels.shape[1]

        c_min = np.zeros(cs)
        c_max = np.zeros(cs)
        for ci in xrange(cs):
            c_min[ci] = np.min(pixels[:, ci])
            c_max[ci] = np.max(pixels[:, ci])

        self._color_range = [c_min, c_max]

    def _computeHistogram(self):
        pixels = self.pixels
        num_bins = self._num_bins
        c_min, c_max = self._color_range

        hist_bins = np.zeros((num_bins, num_bins, num_bins), dtype=np.int32)

        color_ids = (num_bins - 1) * (pixels - c_min) / (c_max - c_min)
        color_ids = np.int32(color_ids)

        for color_id in color_ids:
            hist_bins[color_id[0], color_id[1], color_id[2]] += 1

        self._hist_bins = hist_bins

    def colorIDs(self):
        density_mean = np.mean(self._hist_bins)
        color_ids = np.where(self._hist_bins > density_mean * self._alpha)
        return color_ids

    def colorCoordinates(self):
        color_ids = self.colorIDs()
        color_ids = np.array(color_ids).T

        num_bins = self._num_bins
        c_min, c_max = self._color_range
        color_samples = c_min + (color_ids * (c_max - c_min)) / float(num_bins - 1.0)

        return color_samples

    def colorDensities(self):
        color_densities = np.float32(self._hist_bins[self.colorIDs()])

        density_max = np.max(color_densities)
        color_densities = color_densities / density_max

        return color_densities

    def rgbColors(self):
        color_samples = self.colorCoordinates()
        colors = color_samples
        if self._color_space == "Lab":
            colors = Lab2rgb(np.float32(color_samples.reshape(1, -1, 3))).reshape(-1, 3)

        elif self._color_space == "hsv":
            colors = hsv2rgb(np.float32(color_samples.reshape(1, -1, 3))).reshape(-1, 3)

        colors = np.clip(colors, 0.0, 1.0)
        return colors

    def colorRange(self):
        return self._color_range

    def _axisSetting(self, ax):

        color_ranges = 0.1 * np.int32(10 * np.array(self._color_range)).T

        xrange = color_ranges[0]
        yrange = color_ranges[1]
        zrange = color_ranges[2]

        if self._color_space == "rgb":
            ax.set_xlabel('R')
            ax.set_ylabel('G')
            ax.set_zlabel('B')
        elif self._color_space == "Lab":
            ax.set_xlabel('L')
            ax.set_ylabel('a')
            ax.set_zlabel('b')

        elif self._color_space == "hsv":
            ax.set_xlabel('H')
            ax.set_ylabel('S')
            ax.set_zlabel('V')

        ax.set_xticks(xrange)
        ax.set_yticks(yrange)
        ax.set_zticks(zrange)

        xunit = 0.1 * (xrange[1] - xrange[0])
        yunit = 0.1 * (yrange[1] - yrange[0])
        zunit = 0.1 * (zrange[1] - zrange[0])

        xlim = np.array(xrange)
        xlim[0] += -xunit
        xlim[1] += xunit

        ylim = np.array(yrange)
        ylim[0] += -yunit
        ylim[1] += yunit

        zlim = np.array(zrange)
        zlim[0] += -zunit
        zlim[1] += zunit

        ax.set_xlim3d(xlim)
        ax.set_ylim3d(ylim)
        ax.set_zlim3d(zlim)

    def plot(self, ax):
        color_samples = self.colorCoordinates()
        density_size = self._densitySizes()
        colors = self.rgbColors()

        ax.scatter(color_samples[:, 0], color_samples[:, 1], color_samples[:, 2],
                    color=colors, s=density_size)

        self._axisSetting(ax)

    def _densitySizes(self):
        color_densities = self.colorDensities()

        density_size_min, density_size_max = self._density_size_range
        density_size_factor = density_size_max / density_size_min
        density_size = density_size_min * np.power(density_size_factor, color_densities)
        return density_size
