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
        rv = self.app.get('/js/zut')
        assert rv.status_code == 404
        rv = self.app.get('/js/app.js')
        assert rv.status_code == 200
        assert b"angular" in rv.data
        rv = self.app.get('/css/style.css')
        assert rv.status_code == 200
        assert b"background-color" in rv.data

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
        rv = self.app.get('/details/start.json')
        assert rv.status_code == 200
        node = json.loads(rv.data.decode('utf-8'))
        assert len(node['connections']) == 1
        assert node['url'] == 'start'
        assert node['html'] == 'start'
        assert node['has_path'] == False
        for page in [page for page in site._pages if page != 'start']:
            rv = self.app.get('/details/%s.json' % page)
            assert rv.status_code == 200
            node = json.loads(rv.data.decode('utf-8'))
            assert node['url'] == site._pages[page].url
            assert node['html'] == site._pages[page].html_source

    def test_start(self):
        from Site.Site import Site
        from Main.Configuration import Configuration
        from tests.DummyBrowser import DummyBrowser
        dummy = DummyBrowser(random.random())
        conf = Configuration(['-b', 'Dummy'])
        headers = [('Content-Type', 'application/json')]
        name = str(uuid.uuid4())
        proxy_path = str(uuid.uuid4())
        data = {'browser': 'Dummy', 'proxy_path': proxy_path, 'proxy': "no proxy", 'name': name}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/start', headers=headers, data=json_data)
        site = Site()
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        assert json_returned['gexf'] == etree.tostring(site._gexf_xml).decode('utf-8')
        assert json_returned['current_page'] == site.current
        assert conf.browser == 'Dummy'
        assert conf.proxy_path is None
        assert site.name == name
        assert len(site._pages) == 1
        site = Site()
        headers = [('Content-Type', 'application/json')]
        url = 'http://{0}.url/startpage'.format(str(uuid.uuid4()))
        data = {'url': url}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/get_from_start', headers=headers, data=json_data)
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        assert json_returned['gexf'] == etree.tostring(site._gexf_xml).decode('utf-8')
        assert json_returned['current_page'] == site.current
        assert site.current != 'start'
        action_i = 0
        assert dummy.actions[action_i] == {'action': 'get', 'target': url}
        assert len(site._pages) == 2
        assert site._pages[site._current].url == url
        assert len(dummy.actions) == 1
        rv = self.app.post('/get_from_start', headers=headers, data=json_data)
        assert rv.status_code == 500
        assert len(dummy.actions) == 1
        data = {'browser': 'Dummy', 'proxy_path': proxy_path, 'proxy': "browsermob proxy", 'name': name}
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
        name = str(uuid.uuid4())
        data = {'browser': 'Dummy', 'proxy_path': None, 'proxy': "no proxy", 'name': name}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        self.app.post('/start', headers=headers, data=json_data)
        ###
        site = Site()
        headers = [('Content-Type', 'application/json')]
        url = 'http://{0}.url/startpage'.format(str(uuid.uuid4()))
        data = {'url': url}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/get_from_start', headers=headers, data=json_data)
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        assert json_returned['gexf'] == etree.tostring(site._gexf_xml).decode('utf-8')
        assert json_returned['current_page'] == site.current
        assert site.current != 'start'
        action_i = 0
        assert dummy.actions[action_i] == {'action': 'get', 'target': url}
        ###
        headers = [('Content-Type', 'application/json')]
        css1 = str(uuid.uuid4())
        data = {'css': css1, 'nb': 0}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/add_connection_and_go', headers=headers, data=json_data)
        site = Site()
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        assert json_returned['gexf'] == etree.tostring(site._gexf_xml).decode('utf-8')
        assert json_returned['current_page'] == site.current
        assert len(dummy.actions) == 3
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'find_elements_by_css_selector'
        assert dummy.actions[action_i]['target'] == css1
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'element.click'
        assert dummy.actions[action_i]['target'] == 'new_match_css_%s' % css1
        assert len(site._connections) == 2
        css2 = str(uuid.uuid4())
        data = {'css': css2, 'nb': 0}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.get('/back_to_start.json')
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        assert json_returned['current_page'] == site.current
        assert json_returned['current_page'] == 'start'
#        assert site.get_current_page().url == url
        assert len(site._connections) == 2
        connection_id = [id for id in site._connections if site._connections[id]['from'] == 'start'][0]
        rv = self.app.get('/follow/{0}.json'.format(connection_id))
        assert rv.status_code == 200
        assert len(site._connections) == 3
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'get'
        connection_id = [id for id in site._connections if site._connections[id]['from'] != 'start'][0]
        rv = self.app.get('/follow/{0}.json'.format(connection_id))
        assert rv.status_code == 200
        assert len(site._connections) == 3
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'find_elements_by_css_selector'
        assert dummy.actions[action_i]['target'] == css1
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'element.click'
        assert dummy.actions[action_i]['target'] == 'new_match_css_%s' % css1
        rv = self.app.post('/add_connection_and_go', headers=headers, data=json_data)
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        assert json_returned['gexf'] == etree.tostring(site._gexf_xml).decode('utf-8')
        assert json_returned['current_page'] == site.current
        assert len(dummy.actions) == 8
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'find_elements_by_css_selector'
        assert dummy.actions[action_i]['target'] == css2
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'element.click'
        assert dummy.actions[action_i]['target'] == 'new_match_css_%s' % css2
        assert len(site._connections) == 4
        end_page = site.current
        rv = self.app.get('/back_to_start.json')
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
#        action_i += 1
#        assert dummy.actions[action_i]['action'] == 'get'
#        assert dummy.actions[action_i]['target'] == url
        assert json_returned['current_page'] == site.current
#        assert site.get_current_page().url == url
        data = {'target': end_page}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/follow_existing_connections', headers=headers, data=json_data)
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        assert json_returned['current_page'] == site.current
        assert json_returned['current_page'] == end_page
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'get'
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'find_elements_by_css_selector'
        assert dummy.actions[action_i]['target'] == css1
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'element.click'
        assert dummy.actions[action_i]['target'] == 'new_match_css_%s' % css1
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'find_elements_by_css_selector'
        assert dummy.actions[action_i]['target'] == css2
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'element.click'
        assert dummy.actions[action_i]['target'] == 'new_match_css_%s' % css2
        rv = self.app.get('/follow/{0}.json'.format(connection_id))
        assert rv.status_code == 500
        assert len(dummy.actions) == 13
        rv = self.app.get('/follow/{0}.json'.format(str(uuid.uuid4())))
        assert rv.status_code == 404
        assert len(dummy.actions) == 13
        rv = self.app.get('/back_to_start.json')
        headers = [('Content-Type', 'application/json')]
        url_go = str(uuid.uuid4())
        data = {'url': url_go}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        rv = self.app.post('/go_to_url', headers=headers, data=json_data)
        json_returned = json.loads(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        action_i += 1
        assert dummy.actions[action_i]['action'] == 'get'
        assert dummy.actions[action_i]['target'] == url_go
