"""
This test illustrates how to run a TileStache server in the background and how
to send requests to this server to retrieve tiles.
"""

import os
import signal
import subprocess
import time

import requests

import artefact

expected_image = 'tile.png'
actual_image = 'artefacts/tile_server.png'

def get_tilestache_file(file_name):
    return os.path.join(os.path.dirname(__file__), 'tilestache', file_name)

class TestTileStacheServer(artefact.TestCaseWithArtefacts):

    def setUp(self):
        print os.listdir(os.path.dirname(__file__))
        server_script = get_tilestache_file('tilestache-server.py')
        config_file = get_tilestache_file('tilestache.cfg')
        server = subprocess.Popen([server_script, '-c', config_file],
                                  preexec_fn=os.setsid)
        time.sleep(1) # To let the time to the server to run
        self.tilestache_server = server

    def tearDown(self):
        os.killpg(self.tilestache_server.pid, signal.SIGTERM)

    def test_tilestache_server(self):
        request = requests.get('http://127.0.0.1:8080/example/0/0/0.png')
        self.assertEquals(request.status_code, 200)
        self.assertEquals(request.headers['content-type'], 'image/png')
        with open(actual_image, 'w') as actual:
            actual.write(request.content)
        with open(actual_image) as actual, open(expected_image) as expected:
            self.assertEquals(actual.read(), expected.read())
