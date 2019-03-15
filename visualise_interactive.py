#!/usr/bin/env python3

#written by Danielle Zhang on 24/02/19

import gpxpy
import argparse
import os
import pandas as pd
import numpy as np
from rdp import rdp
import folium
from visualise import read_file


#create interactive map
def interactive(directory):

    map = folium.Map(tiles = "CartoDB dark_matter", location = [-37.81,144.94])
    df_arr = read_file(directory)
    for df in df_arr:
        folium.PolyLine(df, color = "#42bcf4").add_to(map)
        
    map.save('./folium.html')


if __name__ == "__main__":
    interactive('./sample_data/')
