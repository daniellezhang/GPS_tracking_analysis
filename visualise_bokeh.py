#!/usr/bin/env python3

#written by Danielle Zhang on 24/02/19

import gpxpy
import argparse
import os
import pandas as pd
import numpy as np
from rdp import rdp
from bokeh.plotting import show, output_notebook, figure
from bokeh.tile_providers import CARTODBPOSITRON


#create map using bokeh
def bokeh_visualise(directory):

    p = figure(plot_width = 1200, plot_height = 600,x_range=(-1800000, 1800000), y_range=(-900000,9000000),
    x_axis_type="mercator", y_axis_type="mercator")

    p.add_tile(CARTODBPOSITRON)
    show(p)


if __name__ == "__main__":
    bokeh_visualise('./sample_data')
