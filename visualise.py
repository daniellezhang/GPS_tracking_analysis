#written by Danielle Zhang on 03/02/19
import gpxpy
import argparse
import os
import matplotlib.pyplot as pyplot


def main():
    parser = argparse.ArgumentParser()

    directory = ''

    parser.add_argument('-input',help = 'input directory', required = True)

    args = parser.parse_args()
    directory = args.input
    plotdata(directory)


#function to plot the data
def plotdata(directory):
    fig = pyplot.figure(facecolor = '0.05')
    ax = pyplot.Axes(fig, [0., 0., 1., 1.], )
    ax.set_aspect('equal')
    ax.set_axis_off()
    fig.add_axes(ax)
    for filename in os.listdir(directory):
        if '.gpx' in filename:
            lat = [ ]
            lon = [ ]
            gpx_file = open(directory+filename,'r')
            gpx_parser = gpxpy.parse(gpx_file)
            gpx_file.close()
            for track in gpx_parser.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        lat.append(point.latitude)
                        lon.append(point.longitude)
            pyplot.plot(lon, lat, color = 'deepskyblue', lw = 0.2, alpha = 0.8)

    filename = directory + 'visual.png'
    pyplot.savefig(filename, facecolor = fig.get_facecolor(),
    bbox_inches='tight', pad_inches=0, dpi=1000)



main()
