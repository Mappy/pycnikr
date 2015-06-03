"""
This file is a python stylesheet which describes layers and styles for Mapnik.
Describe layers and styles by this way is simple and easy-readable
It is not usable by Mapnik directly, you have to translate it with Pycnik, if
you want to try execute pycnik_sample.py
"""
from pycnik.model import *

# Standard zoom level
Map.TILE_SIZE = 256
Map.LEVEL_NUMBER = 20
Map.ZOOM_FACTOR = 2

# Map definition
Map.background_color = 'rgb(70,130,180)'  # steelblue
#Map.background_color = 'rgb(154, 205, 50)'  # green

Map.srs = '+init=epsg:3857'  # pseudo mercator
Map.minimum_version = '2.0'
Map.buffer_size = 128

# Layers
countries = Layer('countries')
countries.datasource = {
    'type': 'shape',
    'file': '/srv/pycnikr/pycnikr/geo_data/ne_110m_admin_0_countries_merc.shp',
}

zoom_style = {
     POLYGON: {
        'fill': 'rgb(195,211,188)'
    },
}

# Assign th same style for all zoom levels
for zoom in xrange(20):
    countries.style('countries')[zoom] = zoom_style
