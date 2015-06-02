# -*- coding: utf-8 -*-

import os
from os.path import join, dirname
import signal
import subprocess
import time

from django.apps import AppConfig

class TileStacheWrapper(AppConfig):

    name = 'tilestache'
    server = None

    def ready(self):
        if self.__class__.server is None:
            print 'Starting TileStache...'
            cfg_path = join(dirname(__file__), 'tilestache.cfg')
            server = subprocess.Popen(['tilestache-server.py',
                                       '-c', cfg_path,
                                       '-i', '0.0.0.0',
                                       '-p', '8080',
                                       ],
                                      preexec_fn=os.setsid)
            time.sleep(1) # To let the time to the server to run
            if server.poll() is None:
                signal.signal(signal.SIGINT, stop)
                self.__class__.server = server
                print 'TileStache successfully started'
            else:
                print 'Error: failed to start TileStache'
                os.kill(os.getpid(), signal.SIGTERM)

    @classmethod
    def stop(cls):
        print 'Stopping TileStache'
        if cls.server:
            os.kill(cls.server.pid, signal.SIGTERM)
            cls.server = None
            print 'TileStache successfully stopped'
        os.kill(os.getpid(), signal.SIGTERM)


def stop(signum, frame):
    TileStacheWrapper.stop()



