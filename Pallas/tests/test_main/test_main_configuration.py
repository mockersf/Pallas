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
        assert config.auto == False
        assert config.browser == 'PhantomJS'
        proxy_path = str(uuid.uuid4())
        config.proxy_path = proxy_path
        assert config.proxy_path == proxy_path
        config.browser = 'Firefox'
        assert config.browser == 'Firefox'
        config.browser = 'Navigateur Inexistant'
        assert config.browser == 'Firefox'
        config.browser = 'PhantomJS'
        assert config.browser == 'PhantomJS'

    def test_values(self):
        from Main.Configuration import Configuration
        target_url = str(uuid.uuid4())
        path = str(uuid.uuid4())
        for level in [{'DEBUG': 10}, {'INFO': 20}, {'WARNING': 30}, {'ERROR': 40}, {'CRITICAL': 50}, {'FATAL': 50}, {'NOTHING': 50}]:
            config = Configuration(['-v', list(level.keys())[0], '--target', target_url, '--proxy-path', path])
            assert config.log_level == list(level.keys())[0]
            assert config.get_log_level() == level[list(level.keys())[0]]
            assert config.target == target_url
            assert config.proxy_path == path
