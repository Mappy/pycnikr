"""
This script is a sample to understand the behaviour of pycnik translator.
It generates a XML stylesheet from a python stylesheet, qhich is really more
user-friendly.

input  : python stylesheet
output : xml stylesheet and map image

"""
from pycnik import pycnik
import mapnik

python_stylesheet = pycnik.import_style('stylesheet.py')

xml_stylesheet = 'stylesheet.xml'
pycnik.translate(python_stylesheet, xml_stylesheet)

image = 'world.png'
m = mapnik.Map(600, 300)
mapnik.load_map(m, xml_stylesheet)
m.zoom_all()
mapnik.render_to_file(m, image)
print "rendered image to '%s'" % image
