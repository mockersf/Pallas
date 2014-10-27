import os.path
import sys
import uuid
import random

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Test_Main_Action(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_repr_setter_getter(self):
        from Main.Action import Action
        data = str(uuid.uuid4())
        connection = str(uuid.uuid4())
        type = str(uuid.uuid4())
        action = Action(type, data, connection)
        assert "{0}".format(action) == ("<Action ('{0}', '{1}', '{2}')".format(type, data, connection))
        assert action.connection == connection
        assert action.data == data

    def test_do(self):
        from Main.Configuration import Configuration
        from Site.Site import Site
        from Main.Browser import Browser
        from tests.DummyBrowser import DummyBrowser
        dummy = DummyBrowser(random.random())
        config = Configuration(['-b', 'Dummy'])
        config._browser = 'Dummy'
        site_name = str(uuid.uuid4())
        site = Site(site_name)
        browser = Browser(random.random())
        from Main.Action import Action
        url = str(uuid.uuid4())
        connection = str(uuid.uuid4())
        action = Action(str(uuid.uuid4()), '', '')
        action.do()
        assert len(dummy.actions) == 0
