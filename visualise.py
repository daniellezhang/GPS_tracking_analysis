#written by Danielle Zhang on 03/02/19
import gpxpy
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

land_colour = "#000000"
water_colour = "#000000"
boarder_colour = "#d6d6d6"
data_colour = "#196baa"
marker_fill_color = '#cc3300'
marker_edge_color = 'None'

def main():
    parser = argparse.ArgumentParser()

    directory = ''

    parser.add_argument('-input',help = 'input directory', required = True)

    args = parser.parse_args()
    directory = args.input
    plotdata(directory)


#function to plot the data
def plotdata(directory):

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, facecolor='#ffffff', frame_on=False)


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
            df = pd.DataFrame(columns = ['lat','lon'])
            for track in gpx_parser.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        df = df.append({'lat': point.latitude,
                        'lon':point.longitude}, ignore_index = True)

            df['lat'] = df['lat']
            df['lon'] = df['lon']
            x,y = m(df['lon'].values,df['lat'].values)
            m.scatter(x,y, s=8, color=marker_fill_color,
            edgecolor=marker_edge_color, alpha=1, zorder=3)

    filename = directory + 'visual.png'
    plt.savefig(filename, facecolor = fig.get_facecolor(),
    bbox_inches='tight', pad_inches=0, dpi=1000)

    plt.show()



main()
