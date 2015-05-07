"""
This test illustrates how to run a TileStache server in the background and how
to send requests to this server to retrieve tiles.
"""

import os
import signal
import subprocess
import time

import requests

expected_image = 'tile.png'
actual_image = 'artefacts/tile_server.png'

def get_tilestache_file(file_name):
    return os.path.join(os.path.dirname(__file__), 'tilestache', file_name)

server_script = get_tilestache_file('tilestache-server.py')
config_file = get_tilestache_file('tilestache.cfg')

tilestache_server = subprocess.Popen([server_script, '-c', config_file],
                                     preexec_fn=os.setsid)

try:
    time.sleep(1) # To let the time to the server to run
    request = requests.get('http://127.0.0.1:8080/example/0/0/0.png')
    with open(actual_image, 'w') as actual:
        actual.write(request.content)
    assert request.status_code == 200
    assert request.headers['content-type'] == 'image/png'
    with open(actual_image) as actual, open(expected_image) as expected:
        actual_read = expected.read()
except:
    raise
finally:
    os.killpg(tilestache_server.pid, signal.SIGTERM)
