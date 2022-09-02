import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import os.path
from numpy import sin, cos, radians, array

'''To do:
    UI function (change figsize, read in data file?)
    Save image
    '''

SUN_LOCATION = array([(2799), (3872)]) #pixel location of sun in image
LY_LENGTH = 206.0/5000 #number of pixels per light year
INTERPOLATION = 'hanning' #Interpolation needed for antialiasing

parser = argparse.ArgumentParser(description = "Plot points over a top-down image of the galaxy.")
parser.add_argument('--figsize', '-f', type = float, default = 9, help = 'Size of figure in inches')
parser.add_argument('--datafile', '-d', default = 'locations.csv', help = 'File containing location data')
parser.add_argument('--galaxy', '-g', default = 'eso1339e.tif', help = '''Galaxy background file. 
Download from (Original from (https://cdn.eso.org/images/original/eso1339e.tif)''')
parser.add_argument('--savefile', '-s', help = 'Location to save file.')
args = parser.parse_args()


def convert_coords(gal_longitude, gal_latitude, light_year_distance):
    '''Convert the galactic longitude, galactic latitude, and distance in light years to data coordinates'''
    dist = abs(light_year_distance * cos(radians(gal_latitude))) #calculate distance in plane of disk
    angle = radians(gal_longitude + 90) #transform from galactic longitude to radians
    dir_from_sun = array([cos(angle), -sin(angle)]) #unit vector in direction of object
    rel_coords = dist * LY_LENGTH * dir_from_sun #calculate pixels up/down and left/right from sun
    abs_coords = rel_coords + SUN_LOCATION #transform relative to absolute coordinates on image
    return abs_coords



with open(args.datafile, 'r') as f:
    f.readline() #skip header
    raw_data = f.readlines()

data = []

#process raw data into plottable coordinates and labels
for line in raw_data:
    s = line.strip() #remove newline
    if s[-1] != 'Y': #don't plot things without a Y in the display column
        continue
    if ',' not in s:
        raise Exception("You must use a comma to separate values.")
    try:
        glong, glat, dist, label, _ = s.split(',') #split on delimiter
    except ValueError:
        raise Exception('''You must have five values in each row: galactic longitude, 
        galactic latitude, distance in light years, a label, and whether to plot this point.''')
    coords = [float(x) for x in (glong, glat, dist)] #make values floats
    plottable_coords = convert_coords(*coords)
    data.append((plottable_coords, label))



fig = plt.figure(figsize = (args.figsize, args.figsize))
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
img = mpimg.imread(args.galaxy) #Read image data for Milky Way 
ax.imshow(img, interpolation = INTERPOLATION) #Draw background image of Milky Way

#add credit textbox:
ax.text(.02, .02, 'Credit: NASA/JPL-Caltech/ESO/R. Hurt\nhttps://www.eso.org/public/images/eso1339e/', 
        transform = ax.transAxes, color = 'gray', fontsize = 8, bbox = {'fill' : True, 
        'facecolor': 'black', 'alpha' :.5})

for (x, y), label in data:
    ax.scatter(x, y, color = 'black')
    ax.annotate(label, (x, y), xytext = (10, 0), textcoords = 'offset pixels')

ax.scatter(*SUN_LOCATION, color = 'yellow')
ax.annotate('Sun', (SUN_LOCATION[0], SUN_LOCATION[1]), xytext = (10, 0), textcoords = 'offset pixels', color = 'yellow')
plt.show()

if args.savefile:
    filename, extension = args.savefile.split('.')
    counter = 0
    sf = args.savefile
    while os.path.exists(sf):
        counter += 1
        sf = '{}_{}.{}'.format(filename, counter, extension)
    fig.savefig(sf)

