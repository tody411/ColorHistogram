# -*- coding: utf-8 -*-
## @package color_histogram.core.hist_common
#
#  Common color histogram functions for 1D, 2D, 3D.
#  @author      tody
#  @date        2015/08/29

import numpy as np


def colorCoordinates(color_ids, num_bins, color_range):
    color_ids = np.array(color_ids).T
    c_min, c_max = color_range
    color_coordinates = c_min + (color_ids * (c_max - c_min)) / float(num_bins - 1.0)
    return color_coordinates


def colorDensities(hist_bins):
    hist_positive = hist_bins > 0.0
    color_densities = np.float32(hist_bins[hist_positive])

    density_max = np.max(color_densities)
    color_densities = color_densities / density_max

    return color_densities


def rgbColors(hist_bins, color_bins):
    hist_positive = hist_bins > 0.0

    colors = color_bins[hist_positive, :]
    colors = np.clip(colors, 0.0, 1.0)
    return colors


def clipLowDensity(hist_bins, color_bins, alpha):
    density_mean = np.mean(hist_bins)
    low_density = hist_bins < density_mean * alpha
    hist_bins[low_density] = 0.0

    for ci in xrange(3):
        color_bins[low_density, ci] = 0.0


def densitySizes(color_densities, density_size_range):
    density_size_min, density_size_max = density_size_range
    density_size_factor = density_size_max / density_size_min
    density_sizes = density_size_min * np.power(density_size_factor, color_densities)
    return density_sizes


def range2ticks(tick_range, decimals=1):
    ticks = np.around(tick_range, decimals=decimals)
    ticks[ticks > 10] = np.rint(ticks[ticks > 10])
    return ticks


def range2lims(tick_range):
    unit = 0.1 * (tick_range[:, 1] - tick_range[:, 0])
    lim = np.array(tick_range)
    lim[:, 0] += -unit
    lim[:, 1] += unit

    return lim
