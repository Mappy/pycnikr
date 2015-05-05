"""
This script runs a tilestache server in background, and some tile requests are
done to ensure that the server works, and if the tiles which are received are
what we expected
"""
#!/usr/bin/env python

import subprocess
import os
import time
import requests
import signal
from PIL import Image
from StringIO import StringIO

server_script = os.path.join(
    os.path.dirname(__file__),
    'resources_tilestache',
    'tilestache-server.py')

config_file = os.path.join(
    os.path.dirname(__file__),
    'resources_tilestache',
    'tilestache.cfg')

tilestache_server = subprocess.Popen(
    'python {script} -c {file}'.format(script=server_script, file=config_file),
    shell=True,
    preexec_fn=os.setsid)

for sec in range(0,3):
    time.sleep(1)
    request = requests.get('http://127.0.0.1:8080/example/0/0/0.png')
    img_size = Image.open(StringIO(request.content)).size

    assert(request.status_code==200)
    assert(request.headers['content-type']=='image/png')
    assert(img_size[0]==256)
    assert(img_size[1]==256)

os.killpg(tilestache_server.pid, signal.SIGTERM)
