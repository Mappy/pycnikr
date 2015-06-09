"""
This test illustrate how to generate an XML Mapnik style sheet from a pycnik
style sheet written in Python.
"""
import os

from pycnik import pycnik
import artefact

actual_xml_style_sheet = 'artefacts/style_sheet.xml'
expected_xml_style_sheet = 'style_sheet.xml'

class TestPycnik(artefact.TestCaseWithArtefacts):

    def test_pycnik(self):
        python_style_sheet = pycnik.import_style('style_sheet.py')
        pycnik.translate(python_style_sheet, actual_xml_style_sheet)
        with open(actual_xml_style_sheet) as actual, \
                open(expected_xml_style_sheet) as expected:
            self.assertEquals(actual.read(), expected.read())
