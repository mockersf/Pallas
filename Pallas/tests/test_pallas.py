import os.path
import sys
import uuid
import random

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Test_pallas(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_default_run(self):
        import pallas
        from Main.Configuration import Configuration
        from Site.Site import Site
        from Main.Browser import Browser
        from tests.DummyBrowser import DummyBrowser
        dummy = DummyBrowser(random.random())
        config = Configuration(['-b', 'Dummy'])
        config._browser = 'Dummy'
        Browser(random.random())
        pallas.check_website(str(uuid.uuid4()))
