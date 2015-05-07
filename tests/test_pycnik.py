"""
This test illustrate how to generate an XML Mapnik template from a pycnik
stylesheet written in Python.
"""

from pycnik import pycnik

python_stylesheet = pycnik.import_style('stylesheet.py')
actual_xml_stylesheet = 'artefacts/stylesheet.xml'
expected_xml_stylesheet = 'stylesheet.xml'
pycnik.translate(python_stylesheet, actual_xml_stylesheet)
with open(actual_xml_stylesheet) as actual, \
        open(expected_xml_stylesheet) as expected:
    assert actual.read() == expected.read()
