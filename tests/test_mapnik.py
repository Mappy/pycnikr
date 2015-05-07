import mapnik

""" This test illustrate how to Mapnik with an XML stylesheet to generate an
image"""

actual_image = 'artefacts/world.png'
expected_image = 'world.png'
m = mapnik.Map(600, 300)
mapnik.load_map(m, 'stylesheet.xml')
m.zoom_all()
mapnik.render_to_file(m, actual_image)
with open(actual_image) as actual, open(expected_image) as expected:
    assert actual.read() == expected.read()

