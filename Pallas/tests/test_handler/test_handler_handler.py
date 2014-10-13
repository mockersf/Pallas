import os.path
import sys
import uuid
import random
import json
from lxml import etree


def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Test_Handler_Handler(object):
    def setup_method(self, method):
        from Handler.Handler import app
        self.app = app.test_client()

    def teardown_method(self, method):
        pass

    def test_basic(self):
        rv = self.app.get('/')
        assert rv.status_code == 200
        assert b"Pallas" in rv.data

    def test_static(self):
        rv = self.app.get('/s/zut')
        assert rv.status_code == 404
        rv = self.app.get('/s/app.js')
        assert rv.status_code == 200
        assert b"angular" in rv.data

    def test_config(self):
        from Main.Configuration import Configuration
        config = Configuration([])
        rv = self.app.get('/default-target.json')
        config_flask = json.loads(rv.data.decode('utf-8'))
        assert config_flask['browser'] == config.browser
        assert config_flask['url'] == config.target
        assert config_flask['proxy'] == config.proxy_path
        target_url = str(uuid.uuid4())
        path = str(uuid.uuid4())
        browser = random.choice(['Firefox'])
        config = Configuration(['--target', target_url, '--proxy-path', path])
        rv = self.app.get('/default-target.json')
        config_flask = json.loads(rv.data.decode('utf-8'))
        assert config_flask['browser'] == config.browser
        assert config_flask['url'] == config.target
        assert config_flask['proxy'] == config.proxy_path

    def create_site(self):
        from Site.Site import Site
        from Site.Page import Page
        from Main.Action import Action
        site_url = "http://%s.url/for/page" % uuid.uuid4()
        site = Site(site_url)
        node_start = str(uuid.uuid4())
        node_1 = str(uuid.uuid4())
        node_2 = str(uuid.uuid4())
        node_end = str(uuid.uuid4())
        connection_0_id = str(uuid.uuid4())
        connection_0_content = {'from': 'start', 'to': node_start, 'explored': True, 'type': site.ConnectionTypes.START, 'data': {'url': site_url}}
        connection_1_id = str(uuid.uuid4())
        connection_1_url = str(uuid.uuid4())
        connection_1_content = {'from': node_start, 'to': node_1, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': {'url': connection_1_url}}
        connection_2_id = str(uuid.uuid4())
        connection_2_url = str(uuid.uuid4())
        connection_2_content = {'from': node_1, 'to': node_2, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': {'url': connection_2_url}}
        connection_3_id = str(uuid.uuid4())
        connection_3_url = str(uuid.uuid4())
        connection_3_content = {'from': node_2, 'to': node_end, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': {'url': connection_3_url}}
        connection_4_id = str(uuid.uuid4())
        connection_4_url = str(uuid.uuid4())
        connection_4_content = {'from': node_2, 'to': node_1, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': {'url': connection_4_url}}
        connection_5_id = str(uuid.uuid4())
        connection_5_url = str(uuid.uuid4())
        connection_5_content = {'from': node_start, 'to': node_2, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': {'url': connection_5_url}}
        connection_6_id = str(uuid.uuid4())
        connection_6_url = str(uuid.uuid4())
        connection_6_content = {'from': node_end, 'to': None, 'explored': False, 'type': site.ConnectionTypes.LINK, 'data': {'url': connection_6_url}}
        site._connections[connection_0_id] = connection_0_content
        site._connections[connection_1_id] = connection_1_content
        site._connections[connection_2_id] = connection_2_content
        site._connections[connection_3_id] = connection_3_content
        site._connections[connection_4_id] = connection_4_content
        site._connections[connection_5_id] = connection_5_content
        site._connections[connection_6_id] = connection_6_content
        html_start = '<html><body>%s</body></html>' % uuid.uuid4()
        site._pages[node_start] = Page('node_start', html_start)
        html_1 = '<html><body>%s</body></html>' % uuid.uuid4()
        site._pages[node_1] = Page('node_1', html_1)
        html_2 = '<html><body>%s</body></html>' % uuid.uuid4()
        site._pages[node_2] = Page('node_2', html_2)
        html_end = '<html><body>%s</body></html>' % uuid.uuid4()
        site._pages[node_end] = Page('node_end', html_end)
        site._current = node_start
        return site

    def test_get_node(self):
        site = self.create_site()
        rv = self.app.get('/details/zut.json')
        assert rv.status_code == 404
        rv = self.app.get('/details/%s.json' % site._current)
        assert rv.status_code == 200
        for page in site._pages:
            rv = self.app.get('/details/%s.json' % page)
            assert rv.status_code == 200
            node = json.loads(rv.data.decode('utf-8'))
            assert node['url'] == site._pages[page].url
            assert node['html'] == site._pages[page].html_source

    def test_start(self):
        from Site.Site import Site
        from Main.Configuration import Configuration
        conf = Configuration()
        headers = [('Content-Type', 'application/json')]
        url = str(uuid.uuid4())
        proxy_path = str(uuid.uuid4())
        data = {'browser': 'Dummy', 'proxy_path': proxy_path, 'proxy': "no proxy", 'url': url}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/start', headers=headers, data=json_data)
        site = Site()
        assert rv.status_code == 200
        assert conf.browser == 'Dummy'
        assert conf.proxy_path is None
        assert site.url == url
        assert len(site._pages) == 1
        assert site._pages[site._current].url == url
        assert rv.data == etree.tostring(site.get_gexf())
        data = {'browser': 'Dummy', 'proxy_path': proxy_path, 'proxy': "browsermob proxy", 'url': url}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/start', headers=headers, data=json_data)
        assert conf.proxy_path == proxy_path

    def test_add_connection(self):
        from Site.Site import Site
        from Main.Configuration import Configuration
        from tests.DummyBrowser import DummyBrowser
        dummy = DummyBrowser(random.random())
        conf = Configuration()
        headers = [('Content-Type', 'application/json')]
        url = str(uuid.uuid4())
        data = {'browser': 'Dummy', 'proxy_path': None, 'proxy': "no proxy", 'url': url}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        self.app.post('/start', headers=headers, data=json_data)
        headers = [('Content-Type', 'application/json')]
        css = str(uuid.uuid4())
        data = {'css': css, 'nb': 0}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/add_connection_and_go', headers=headers, data=json_data)
        site = Site()
        assert rv.status_code == 200
        assert rv.data == etree.tostring(site.get_gexf())
        assert len(dummy.actions) == 3
        assert dummy.actions[0] == {'action': 'get', 'target': url}
        assert dummy.actions[1]['action'] == 'find_elements_by_css_selector'
        assert dummy.actions[1]['target'] == css
        assert dummy.actions[2]['action'] == 'element.click'
        assert dummy.actions[2]['target'] == 'new_match_css_%s' % css
