
# -*- coding: utf-8 -*-
## @package color_histogram.core.hist_3d
#
#  Color histogram 3D class.
#  @author      tody
#  @date        2015/08/28

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from color_histogram.cv.image import to32F, rgb, hsv2rgb, Lab2rgb
from color_histogram.datasets.google_image import loadData


## Implementation of 3D color histograms.
class Hist3D:
    ## Constructor
    #  @param image          input image.
    #  @param num_bins       target number of histogram bins.
    #  @param alpha          low density clip.
    def __init__(self, image,
                 num_bins=16, alpha=0.3, color_space="rgb"):
        self._pixels = self.toPixels(image)
        self._num_bins = num_bins
        self._alpha = alpha
        self._color_space = color_space

        self.computeColorRanges()
        self.computeHistogram()

    def toPixels(self, image):
        if len(image.shape) == 2:
            h, w = image.shape
            return image.reshape((h * w))

        h, w, cs = image.shape
        return image.reshape((-1, cs))

    def computeColorRanges(self):
        pixels = self._pixels

        cs = pixels.shape[1]

        c_min = np.zeros(cs)
        c_max = np.zeros(cs)
        for ci in xrange(cs):
            c_min[ci] = np.min(pixels[:, ci])
            c_max[ci] = np.max(pixels[:, ci])

        self._color_ranges = [c_min, c_max]

    def computeHistogram(self):
        pixels = self._pixels
        num_bins = self._num_bins
        c_min, c_max = self._color_ranges

        hist_bins = np.zeros((num_bins, num_bins, num_bins), dtype = np.int32)

        num_pixels = pixels.shape[0]
        color_ids = (num_bins - 1) * (pixels - c_min) / (c_max-c_min)
        color_ids = np.int32(color_ids)

        for color_id in color_ids:
            hist_bins[color_id[0], color_id[1], color_id[2]] += 1

        self._hist_bins = hist_bins

    def colorIDs(self):
        density_mean = np.mean(self._hist_bins)
        color_ids = np.where(self._hist_bins > density_mean * self._alpha)
        return color_ids

    def colorSamples(self):
        color_ids = self.colorIDs()
        color_ids = np.array(color_ids).T
        print color_ids.shape

        num_bins = self._num_bins
        c_min, c_max = self._color_ranges
        color_samples = c_min + (color_ids * (c_max - c_min)) / float(num_bins - 1.0)

        return color_samples

    def colorDensities(self):
        color_densities = np.float32(self._hist_bins[self.colorIDs()])

        density_max = np.max(color_densities)
        color_densities = color_densities / density_max

        return color_densities

    def rgbColors(self):
        color_samples = self.colorSamples()
        colors = color_samples
        if self._color_space == "Lab":
            colors = Lab2rgb(np.float32(color_samples.reshape(1, -1, 3))).reshape(-1, 3)

        elif self._color_space == "hsv":
            colors = hsv2rgb(np.float32(color_samples.reshape(1, -1, 3))).reshape(-1, 3)

        colors = np.clip(colors, 0.0, 1.0)
        return colors

    def colorRanges(self):
        return self._color_ranges

    def axisColorSpace(self, ax):

        color_ranges = 0.1 * np.int32(10 * np.array(self._color_ranges)).T

        xrange = color_ranges[0]
        yrange = color_ranges[1]
        zrange = color_ranges[2]

        if self._color_space == "rgb":
            ax.set_xlabel('R')
            ax.set_ylabel('G')
            ax.set_zlabel('B')
        elif self._color_space == "Lab":
#             xrange = [0.0, 100.0]
#             yrange = [-50, 100.0]
#             zrange = [-50.0, 100.0]

            ax.set_xlabel('L')
            ax.set_ylabel('a')
            ax.set_zlabel('b')

        elif self._color_space == "hsv":
#             xrange = [0.0, 360.0]
#             yrange = [0.0, 1.0]
#             zrange = [0.0, 1.0]

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

    def plotColorSamples(self, ax):
        color_samples = self.colorSamples()
        density_size = self.plotDensitySize()
        colors = self.rgbColors()

        ax.scatter(color_samples[:, 0], color_samples[:, 1], color_samples[:, 2],
                    color=colors, s=density_size)

        self.axisColorSpace(ax)







    def plotDensitySize(self):
        color_densities = self.colorDensities()
        density_size = 10.0 * np.power(10.0, color_densities)
        return density_size


if __name__ == '__main__':
    C_8U = loadData(data_name="flower", data_id=0)
    rgb_8U = rgb(C_8U)
    C_32F = to32F(rgb_8U)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    hist3D = Hist3D(C_32F, num_bins=16)
    hist3D.plotColorSamples(ax)

    plt.show()