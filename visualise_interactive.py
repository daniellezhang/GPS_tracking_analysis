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
from visualise import read_file


#create interactive map
def interactive(directory):

    df_arr = read_file(directory)
    p = figure(plot_width = 1200,
     plot_height = 600,
    x_axis_type="mercator",
     y_axis_type="mercator")

    p.add_tile(CARTODBPOSITRON)
    for df in df_arr:
        p.line(x = df['lon'],y = df['lat'], line_width=2, line_color="blue")
    show(p)


if __name__ == "__main__":
    interactive('./sample_data/')
