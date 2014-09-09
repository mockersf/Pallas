from urlparse import urlparse

from Page import Page

class Site:
    _url = None
    _pages = None
    
    def __init__(self, url):
        self._url = url
        self._pages = []

    def __repr__(self):
        return "<Site ('%s')" % (self._url)
    
    @property
    def url(self):
        return self._url
    
    @property
    def hostname(self):
        return urlparse(self._url).hostname