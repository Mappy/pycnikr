"""
This script is a sample to understand the behaviour of pycnik translator.
It generates a XML stylesheet from a python stylesheet, which is really more
user-friendly to describe layers and styles than XML stylesheet

input  : python stylesheet (stylesheet.py)
output : xml stylesheet (stylesheet.xml)
"""

from pycnik import pycnik

python_stylesheet = pycnik.import_style('stylesheet.py')
xml_stylesheet = 'stylesheet.xml'
pycnik.translate(python_stylesheet, xml_stylesheet)
