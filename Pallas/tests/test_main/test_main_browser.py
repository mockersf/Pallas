import os.path
import sys
import uuid
import random

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Test_Main_Browser(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_basic(self):
        from Main.Configuration import Configuration
        from Site.Site import Site
        from Main.Browser import Browser
        from tests.DummyBrowser import DummyBrowser
        dummy = DummyBrowser(random.random())
        config = Configuration(['-b', 'Dummy'])
        config._browser = 'Dummy'
        site_url = str(uuid.uuid4())
        site = Site(site_url)
        browser = Browser(random.random())
        browser.start(site)
        browser.get()
        browser.study_state()
        assert len(dummy.actions) == 3
        assert dummy.actions[0] == {'action': 'get', 'target': site_url}
        assert dummy.actions[1]['action'] == 'find_elements_by_tag_name'
        assert dummy.actions[1]['target'] == 'input'
        assert dummy.actions[2]['action'] == 'find_elements_by_tag_name'
        assert dummy.actions[2]['target'] == 'a'
        assert len(site._pages) == 1
        assert len(site._connections) == dummy.actions[2]['nb'] + 1
        assert len(site._connections) > 1
        assert len([explored for explored in list(site._connections.values()) if explored['explored']]) == 1
        actions = site.get_first_connection_unexplored()
        assert len(actions) == 1
        actions[0].do()
        assert len(dummy.actions) == 5
        assert dummy.actions[3]['action'] == 'find_element_by_xpath'
        assert dummy.actions[4]['action'] == 'element.click'
        browser.stop()
        assert len(dummy.actions) == 6
        assert dummy.actions[5]['action'] == 'quit'

    def test_with_browsermobproxy(self):
        from Main.Configuration import Configuration
        from Site.Site import Site
        from Main.Browser import Browser
        from tests.DummyBrowser import DummyBrowser
        dummy = DummyBrowser(random.random())
        config = Configuration(['-b', 'Dummy', '--env', '--proxy-path', '/home/vagrant/browsermob-proxy-2.0-beta-9/bin/'])
        assert config.proxy_path is not None
        config._browser = 'Dummy'
        site_url = str(uuid.uuid4())
        site = Site(site_url)
        browser = Browser(random.random())
        browser.start(site)
        browser.add_remap_urls(['localhost'])
        browser.get()
        browser.study_state()
        assert len(dummy.actions) == 3
        assert dummy.actions[0] == {'action': 'get', 'target': site_url}
        assert dummy.actions[1]['action'] == 'find_elements_by_tag_name'
        assert dummy.actions[1]['target'] == 'input'
        assert dummy.actions[2]['action'] == 'find_elements_by_tag_name'
        assert dummy.actions[2]['target'] == 'a'
        assert len(site._pages) == 1
        assert len(site._connections) == dummy.actions[2]['nb'] + 1
        assert len(site._connections) > 1
        assert len([explored for explored in list(site._connections.values()) if explored['explored']]) == 1
        actions = site.get_first_connection_unexplored()
        assert len(actions) == 1
        actions[0].do()
        assert len(dummy.actions) == 5
        assert dummy.actions[3]['action'] == 'find_element_by_xpath'
        assert dummy.actions[4]['action'] == 'element.click'
        browser.stop()
        assert len(dummy.actions) == 6
        assert dummy.actions[5]['action'] == 'quit'
