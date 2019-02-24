#!/usr/bin/env python3

#written by Danielle Zhang on 03/02/19
import gpxpy
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from rdp import rdp

#aesthetic of the visualisation
land_colour = "#2d3347"
water_colour = "#2d3347"
boarder_colour = "#ffffff"
marker_fill_color = "#18a9a7"
marker_edge_color = 'None'

def main():
    parser = argparse.ArgumentParser()

    directory = ''

    parser.add_argument('-input',help = 'input directory', required = True)

    args = parser.parse_args()
    directory = args.input
    plotdata(directory)

#reduce the number of points to be ploted using ramer–douglas–peucker algorithm
def optimise(arr):
    e = 0.00001
    smoothed_arr = rdp(arr, epsilon = e)
    smoothed_df = pd.DataFrame({'lon': smoothed_arr[:,0], 'lat':smoothed_arr[:,1]})
    return smoothed_df

#function to plot the data
def plotdata(directory):

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, facecolor='#2d3347', frame_on=False)


    m = Basemap(projection='robin',lon_0=0,resolution='c')
    m.drawcoastlines(color = boarder_colour)
    m.drawmapboundary(fill_color=water_colour)
    m.fillcontinents(color = land_colour)
    m.drawcountries(color = boarder_colour)


    for filename in os.listdir(directory):
        if filename.split('.')[-1] == 'gpx':
            gpx_file = open(directory+filename,'r')
            gpx_parser = gpxpy.parse(gpx_file)
            gpx_file.close()

            n_points = 0
            arr = np.empty((0))
            for track in gpx_parser.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        n_points += 1
                        arr = np.append(arr, [point.longitude,point.latitude] )

            arr = np.reshape(arr, (n_points,2))
            smoothed_df = optimise(arr)
            x,y = m(smoothed_df['lon'].values,smoothed_df['lat'].values)
            m.plot(x,y,color=marker_fill_color)

    filename = directory + 'visual.png'
    plt.savefig(filename, facecolor = fig.get_facecolor(),
    bbox_inches='tight', pad_inches=0, dpi=1000)

    plt.show()


main()
