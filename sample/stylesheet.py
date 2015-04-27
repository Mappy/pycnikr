from pycnik.model import *

# Standard zoom level
Map.TILE_SIZE = 256
Map.LEVEL_NUMBER = 20
Map.ZOOM_FACTOR = 2

# Map definition
Map.background_color = 'rgb(70,130,180)'  # steelblue
Map.srs = '+init=epsg:3857'  # pseudo mercator
Map.minimum_version = '2.0'
Map.buffer_size = 128

# Layers
countries = Layer('countries')
countries.datasource = {
    'type': 'shape',
    'file': 'data/ne_110m_admin_0_countries.shp',
}

countries.style()[1] = {
     POLYGON: {
        'fill': 'rgb(195,211,188)'
    },
}

for zoom_level in (2,19):
    countries.style()[zoom_level] = countries.style()[1]






