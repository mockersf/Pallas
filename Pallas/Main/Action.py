import logging

from Main.Browser import Browser


class Action:
    _type = None
    _data = None
    _connection = None

    class ActionType:
        CLICK = "click"
        FILL = "fill"
        GET = 'get'

    def __init__(self, type, data, connection=None):
        self._type = type
        self._data = data
        self._connection = connection

    def __repr__(self):
        return "<Action ('%s', '%s', '%s')" % (self._type, self._data, self._connection)

    def do(self):
        try:
            if self._type == self.ActionType.GET:
                browser = Browser()
                browser.get(self._data['url'])
                return
            if self._type == self.ActionType.CLICK:
                browser = Browser()
                browser.click(self)
                return
            raise Exception('unknown action type')
        except Exception as e:
            logging.warning("couldn't do action {0} : {1}".format(self, e))

    @property
    def connection(self):
        return self._connection

    @property
    def data(self):
        return self._data
