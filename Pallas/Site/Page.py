class Page(object):
    _url = None
    _title = None
    _interests = None
    _calls = None
    _name = None

    def __init__(self, url, html_source):
        self._url = url
        self._html_source = html_source
        self._interests = []
        self._calls = []
        self._name = None

    def __repr__(self):
        return "<Page ('%s', '%s')>" % (self._name, self._url)

    def add_interest(self, interest):
        interest['explored'] = False
        self._interests.append(interest)

    def add_call(self, call):
        self._calls.append(call)

    @property
    def url(self):
        return self._url

    @property
    def html_source(self):
        return self._html_source

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
