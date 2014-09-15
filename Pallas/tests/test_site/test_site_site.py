import os.path
import sys


def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class Test_Site_Site(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_getting_hostname(self):
        from Site.Site import Site
        site = Site('http://google.com/')
        assert site.hostname == 'google.com'

    def test_adding_one_page(self):
        from Site.Site import Site
        site = Site('http://google.com/')
        assert len(site._pages) == 0
        site.current_page("<html></html>", 'http://google.com/')
        assert len(site._pages) == 1

    def test_adding_two_page(self):
        from Site.Site import Site
        site = Site('http://google.com/')
        assert len(site._pages) == 0
        site.current_page("<html></html>", 'http://google.com/')
        site.current_page("<html><body></body></html>", 'http://google.com/2')
        assert len(site._pages) == 2

    def test_adding_same_page_twice(self):
        from Site.Site import Site
        site = Site('http://google.com/')
        assert len(site._pages) == 0
        site.current_page("<html></html>", 'http://google.com/')
        site.current_page("<html></html>", 'http://google.com/')
        assert len(site._pages) == 1
