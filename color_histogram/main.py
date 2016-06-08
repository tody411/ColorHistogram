
# -*- coding: utf-8 -*-
# # @package color_histogram.main
#
#  Main functions.
#  @author      tody
#  @date        2015/08/28

from color_histogram.results.hist_1d import histogram1DResults
from color_histogram.results.hist_2d import histogram2DResults
from color_histogram.results.hist_3d import histogram3DResults

if __name__ == '__main__':
    data_names = ["apple"]
    num_images = 3
    data_ids = range(num_images)

    histogram1DResults(data_names, data_ids, num_bins=10)
    histogram2DResults(data_names, data_ids, num_bins=10)
    histogram3DResults(data_names, data_ids, num_bins=10)
