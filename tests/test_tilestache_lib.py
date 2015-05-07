"""
This script is a sample to understand how to create a tile with TileStache
It uses the Mapnik XML template and request mapnik for a tile
"""

import TileStache
import ModestMaps

config = {
  "cache": {"name": "Test"},
  "layers": {
    "example": {
        "provider": {"name": "mapnik", "mapfile": "stylesheet.xml"},
        "projection": "spherical mercator"
    }
  }
}

# like http://tile.openstreetmap.org/1/0/0.png
coord = ModestMaps.Core.Coordinate(0, 0, 0)
config = TileStache.Config.buildConfiguration(config)
type, bytes = TileStache.getTile(config.layers['example'], coord, 'png')

open('tile.png', 'w').write(bytes)
