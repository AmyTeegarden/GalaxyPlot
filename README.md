#GalaxyPlot 

Plots points given in galactic longitude, galactic latitude, and distance in light years over an image of the Milky Way.

You will need to download this image: https://cdn.eso.org/images/original/eso1339e.tif and either put it in the same folder as the script or pass the location of the file to the program using the --savefile option.

This website has galactic coordinates for a large number of objects: http://simbad.u-strasbg.fr/simbad/. Look for the Gal coord. line and use the first number in the galactic longitude column of locations.csv and the second number in the galactic latitude column. Simbad doesn't always have the distance, and when it does, it's usually in parsecs. Be sure to convert parsecs to light years before adding the value to the distance column! If Simbad doesn't have the distance at all, check Wikipedia. 