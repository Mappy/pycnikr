"""
Create the output directory which contains all artefacts generated when passing
tests
"""
import os

import unittest

output_dir= 'artefacts'

class TestCaseWithArtefacts(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)