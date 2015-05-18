"""
This test illustrate how to generate an XML Mapnik template from a pycnik
stylesheet written in Python.
"""
import os

from pycnik import pycnik
import artefact

actual_xml_stylesheet = 'artefacts/stylesheet.xml'
expected_xml_stylesheet = 'stylesheet.xml'

class TestPycnik(artefact.TestCaseWithArtefacts):

    def test_pycnik(self):
        python_stylesheet = pycnik.import_style('stylesheet.py')
        pycnik.translate(python_stylesheet, actual_xml_stylesheet)
        with open(actual_xml_stylesheet) as actual, \
                open(expected_xml_stylesheet) as expected:
            self.assertEquals(actual.read(), expected.read())
