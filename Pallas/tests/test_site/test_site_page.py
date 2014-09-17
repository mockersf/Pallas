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
        assert page._interests == []
        page.add_interest({'test': True})
        assert page._interests[0] == {'test': True, 'explored': False}

    def test_calls(self):
        from Site.Page import Page
        page = Page('http://google.com/')
        assert page._calls == []
        page.add_call({'test': True})
        assert page._calls[0] == {'test': True}

    def test_repr(self):
        from Site.Page import Page
        url = "http://test.url/for/page"
        page = Page(url)
        assert page.__repr__() == ("<Page ('%s')>" % (url))