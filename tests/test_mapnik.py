""" This test illustrate how to call Mapnik with an XML stylesheet to
generate an image"""

import mapnik
import os

import artefact

actual_image = 'artefacts/world.png'
expected_image = 'world.png'

class TestMapnik(artefact.TestCaseWithArtefacts):

    def test_mapnik(self):
        m = mapnik.Map(600, 300)
        mapnik.load_map(m, 'stylesheet.xml')
        m.zoom_all()
        mapnik.render_to_file(m, actual_image)
        with open(actual_image) as actual, open(expected_image) as expected:
            self.assertEquals(actual.read(), expected.read())

