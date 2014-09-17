class Page:
    _url = None
    _title = None
    _interests = None
    _calls = None

    def __init__(self, url):
        self._url = url
        self._interests = []
        self._calls = []

    def __repr__(self):
        return "<Page ('%s')>" % (self._url)

    def add_interest(self, interest):
        interest['explored'] = False
        self._interests.append(interest)

    def add_call(self, call):
        self._calls.append(call)
