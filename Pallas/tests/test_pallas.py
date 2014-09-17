import os.path
import sys
import uuid

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Test_pallas(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_getting_hostname(self):
        import pallas
