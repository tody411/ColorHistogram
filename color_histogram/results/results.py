# -*- coding: utf-8 -*-
## @package color_histogram.results.results
#
#  Results utility package.
#  @author      tody
#  @date        2015/08/20

import os
from color_histogram.datasets.google_image import dataFile

_root_dir = os.path.dirname(__file__)


## Result directory.
def resultDir():
    return _root_dir


## Result file.
def resultFile(image_name, image_ext=".png"):
    result_file = os.path.join(resultDir(), image_name + image_ext)
    return result_file


def batchResults(data_names, data_ids, batch_func, batch_name):
    for data_name in data_names:
        print "%s: %s" % (batch_name, data_name)
        for data_id in data_ids:
            print "Data ID: %s" % data_id
            image_file = dataFile(data_name, data_id)
            batch_func(image_file)

if __name__ == '__main__':
    print resultDir()
    print resultFile("testImage")