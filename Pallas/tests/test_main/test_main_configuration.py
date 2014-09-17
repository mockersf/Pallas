import os.path
import sys
import uuid
import logging

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class Test_Main_Configuration(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_defaults(self):
        from Main.Configuration import Configuration
        config = Configuration([])
        assert config.get_log_level() == logging.INFO
        assert config.target == 'http://localhost/'
        assert config.proxy_path is None