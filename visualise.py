#!/usr/bin/env python3
#python ./visualise.py -input ./sample_data/ -latitude -37.8136 -longitude 144.9631
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
water_colour = "#12141c"
boarder_colour = "#ffffff"
marker_fill_color = "#18a9a7"
marker_edge_color = 'None'

#default width and height of the map when a centre coordinate is given, in metres
map_width = 12*1000
map_height = 10*1000

#approximate conversion from 1 degre of latitude and longitude to metres
lat_conversion = 110.574*1000
lon_conversion = 111.320*1000

def main():
    parser = argparse.ArgumentParser()

    directory = ''

    parser.add_argument('-input',help = 'input directory', required = True)
    parser.add_argument('-longitude',help = 'The longitude of the \
    centre of the visualisation. Default is world map', required = False)
    parser.add_argument('-latitude',help = 'The latitude of the \
    centre of the visualisation. Default is world map', required = False)
    args = parser.parse_args()
    directory = args.input
    longitude = args.longitude
    latitude = args.latitude

    plotdata(directory,longitude, latitude)

#reduce the number of points to be ploted using ramer–douglas–peucker algorithm
def optimise(arr):
    e = 0.00001
    smoothed_arr = rdp(arr, epsilon = e)
    #smoothed_df = pd.DataFrame({'lon': smoothed_arr[:,0], 'lat':smoothed_arr[:,1]})
    return smoothed_arr

#check if the point is in the map. return false if the point isn't inside the map
def map_check(lon, lat, centre_lon, centre_lat):
    # approximate the corner?!?
    if abs(centre_lon-lon)*lon_conversion < map_width/2 and \
    abs(centre_lat-lat)*lat_conversion < map_height/2:
        return True

    return False


def read_file(directory):
    data_arr = []
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
                        arr = np.append(arr, [point.latitude,point.longitude])


            arr = np.reshape(arr, (n_points,2))
            smoothed_arr = optimise(arr)
            data_arr.append(smoothed_arr)

    return data_arr

#function to plot the data
def plotdata(directory,longitude, latitude):
    #setting up the map
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, facecolor='#2d3347', frame_on=False)

    if longitude and latitude:
        m = Basemap(projection='tmerc', lon_0 = longitude, lat_0 = latitude,
         width = map_width,height = map_height)
    else:
        m = Basemap(projection='robin',lon_0=0,resolution='c')

    m.drawcoastlines(color = boarder_colour)
    m.drawmapboundary(fill_color=water_colour)
    m.fillcontinents(color = land_colour)
    m.drawcountries(color = boarder_colour)


    data_arr = read_file(directory)
    for arr in data_arr:
        df = pd.DataFrame({'lon': arr[:,1], 'lat':arr[:,0]})
        x,y = m(df['lon'].values,df['lat'].values)
        m.plot(x,y,color=marker_fill_color)

    filename = directory + 'visual.png'
    plt.savefig(filename, facecolor = fig.get_facecolor(),
    bbox_inches='tight', pad_inches=0, dpi=1000)



if __name__ == "__main__":
    main()
