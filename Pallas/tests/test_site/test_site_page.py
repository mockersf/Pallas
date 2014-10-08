import os.path
import sys
import uuid


def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class Test_Site_Site(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_interests(self):
        from Site.Page import Page
        html = '<html><body>%s</body></html>' % uuid.uuid4()
        page = Page('http://google.com/', html)
        assert page._interests == []
        page.add_interest({'test': True})
        assert page._interests[0] == {'test': True, 'explored': False}

    def test_calls(self):
        from Site.Page import Page
        html = '<html><body>%s</body></html>' % uuid.uuid4()
        page = Page('http://google.com/', html)
        assert page._calls == []
        page.add_call({'test': True})
        assert page._calls[0] == {'test': True}

    def test_repr_setter_getter(self):
        from Site.Page import Page
        url = str(uuid.uuid4())
        html = '<html><body>%s</body></html>' % uuid.uuid4()
        page = Page(url, html)
        assert page.__repr__() == ("<Page ('None', '%s')>" % (url))
        assert page.url == url
        assert page.html_source == html
        assert page.name is None
        name = str(uuid.uuid4())
        page.name = name
        assert page.__repr__() == ("<Page ('%s', '%s')>" % (name, url))
        assert page.url == url
        assert page.name == name
