import os.path
import sys

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Test_imports(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_Page(self):
        from Site.Page import Page
        page = Page('http://tests.com')

    def test_Configuration(self):
        from Main.Configuration import Configuration

    def test_Browser(self):
        from Main.Browser import Browser
