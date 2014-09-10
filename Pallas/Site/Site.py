from urlparse import urlparse
import hashlib

from Page import Page

class Site:
    _url = None
    _pages = None
    
    def __init__(self, url):
        self._url = url
        self._pages = {}

    def __repr__(self):
        return "<Site ('%s')" % (self._url)
    
    @property
    def url(self):
        return self._url
    
    @property
    def hostname(self):
        return urlparse(self._url).hostname
    
    def current_page(self, html_source):
        md5 = hashlib.md5(html_source.encode('utf-8')).hexdigest()
        if md5 not in self._pages:
            self._pages[md5] = Page()
        return self._pages[md5]