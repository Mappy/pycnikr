import mapnik

image = 'world.png'
m = mapnik.Map(600, 300)
mapnik.load_map(m, 'stylesheet.xml')
m.zoom_all()
mapnik.render_to_file(m, image)
print "rendered image to '%s'" % image