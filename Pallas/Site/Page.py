import uuid


class Page:
    _url = None
    _id = None
    _title = None
    _interests = None
    _calls = None

    def __init__(self, url):
        self._url = url
        self._id = uuid.uuid4()
        self._interests = []
        self._calls = []

    def __repr__(self):
        return "<Page ('%s')" % (self._id)

    def add_interest(self, interest):
        self._interests.append(interest)

    def add_call(self, call):
        self._calls.append(call)
