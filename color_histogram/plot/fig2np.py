# -*- coding: utf-8 -*-
# # @package color_histogram.plot.fig2np
#
#  color_histogram.plot.fig2np utility package.
#  @author      tody
#  @date        2016/06/08


import numpy as np


# #  Convert matplot figure to numpy.array
def figure2numpy(fig, call_draw=True):
    if call_draw:
        fig.canvas.draw()

    fig_data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    image = fig_data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image
