import os.path
import sys


def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class Test_Site_Site(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_interests(self):
        from Site.Page import Page
        page = Page('http://google.com/')
        page.add_interest({'test': True})
        assert page._interests[0]['explored'] == False
