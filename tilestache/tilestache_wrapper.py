# -*- coding: utf-8 -*-

import os
from os.path import join, dirname
import signal
import subprocess
import time

from django.apps import AppConfig
from django.conf import settings
from django.template import Context, Template

class TileStacheWrapper(AppConfig):

    name = 'tilestache'
    server = None

    def ready(self):

        print 'Generation TileStache configuration...'
        layers = settings.PYCNIKR_STYLE_SHEETS_MAPPING
        layers_for_tpl = {key:value[1] for key, value in layers.items()}
        cfg_template_path = join(dirname(__file__), 'tilestache.cfg.tpl')
        cfg_file_path = join(dirname(__file__), 'tilestache.cfg')
        with open(cfg_template_path, "r") as cfg_template:
            t = Template(cfg_template.read())
            c = Context({'layers': layers_for_tpl})
            with open(cfg_file_path, "w") as cfg_file:
                cfg_file.write(t.render(c))

        # Start the server
        if self.__class__.server is None:
            print 'Starting TileStache...'
            server = subprocess.Popen(['tilestache-server.py',
                                       '-c', cfg_file_path,
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



