"""
This test illustrates how to create a tile with the TileStache library.
It uses the Mapnik engine and a Mapnik XML template.
"""

import os
from StringIO import StringIO

import ModestMaps
from PIL import Image
import TileStache

import artefact

actual_image = 'artefacts/tile_lib.png'
expected_image = 'tile.png'

def get_tilestache_file(file_name):
    return os.path.join(os.path.dirname(__file__), 'tilestache', file_name)

class TestTileStacheLib(artefact.TestCaseWithArtefacts):

    def test_tilestache_lib(self):
        config = eval(open(get_tilestache_file('tilestache.cfg')).read())
        config["layers"]["example"]["provider"]["mapfile"] = "stylesheet.xml"
        # like http://tile.openstreetmap.org/1/0/0.png
        coord = ModestMaps.Core.Coordinate(0, 0, 0)
        config = TileStache.Config.buildConfiguration(config)
        mime_type, image_bytes = TileStache.getTile(config.layers['example'],
                                                    coord,
                                                    'png')
        self.assertEquals(mime_type, 'image/png')
        open(actual_image, 'w').write(image_bytes)
        with open(actual_image) as actual, open(expected_image) as expected:
            actual_read = actual.read()
            self.assertEquals(actual_read, expected.read())
            img = Image.open(StringIO(actual_read))
            self.assertEquals(img.size, (256, 256))
