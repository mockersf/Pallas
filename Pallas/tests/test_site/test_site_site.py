import os.path
import sys
import uuid
import hashlib
from lxml import etree

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class Test_Site_Site(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_singleton(self):
        from Site.Site import Site
        name = str(uuid.uuid4())
        site = Site(name)
        assert site.name == name
        site2 = Site()
        assert site.name == name

#    def test_getting_hostname(self):
#        from Site.Site import Site
#        host = '%s.url' % uuid.uuid4()
#        site = Site('http://%s/' % host)
#        assert site.hostname == host

    def test_adding_one_page(self):
        from Site.Site import Site
        site = Site('%s.url' % uuid.uuid4())
        assert len(site._pages) == 1
        url = str(uuid.uuid4())
        page = site.current_page("<html></html>", url)
        assert len(site._pages) == 2
        assert page._url == url
        assert page._interests == []
        assert page._calls == []

    def test_adding_two_page(self):
        from Site.Site import Site
        site = Site('%s.url' % uuid.uuid4())
        assert len(site._pages) == 1
        site.current_page("<html></html>", 'http://google.com/')
        site.current_page("<html><body></body></html>", 'http://google.com/2')
        assert len(site._pages) == 3

    def test_adding_same_page_twice(self):
        from Site.Site import Site
        site = Site('%s.url' % uuid.uuid4())
        assert len(site._pages) == 1
        page = site.current_page("<html></html>", 'http://google.com/')
        assert len(site._pages) == 2
        call = str(uuid.uuid4())
        page.add_call(call)
        page2 = site.current_page("<html></html>", 'http://google.com/')
        assert len(site._pages) == 2
        assert page2._calls == [call]

    def test_repr_getter(self):
        from Site.Site import Site
        name = str(uuid.uuid4())
        site = Site(name)
        assert site.__repr__() == ("<Site ('{0}')>".format(name))
        assert site.name == name
        assert site.current == 'start'
        assert site.current == site._current

    def test_add_link(self):
        from Site.Site import Site
        url = "http://%s.url/for/page" % uuid.uuid4()
        site = Site(url)
        current_page = uuid.uuid4()
        site._current = current_page
        url = 'http://test.com/about.html'
        connection1 = {'from': current_page, 'type': Site().ConnectionTypes.LINK, 'explored': False, 'to': None, 'data': {'url': url}}
        site.add_link(url)
        assert len(site._connections) == 1
        connection_check = connection1
        connection_check['data'] = {'url': url, 'nb': 0, 'css': '[href="{0}"]'.format(url)}
        assert list(site._connections.values())[0] == connection_check
        site.add_link(url)
        assert len(site._connections) == 1

    def test_get_action(self):
        from Site.Site import Site
        from Main.Action import Action
        site_url = "http://%s.url/for/page" % uuid.uuid4()
        site = Site(site_url)
        url = str(uuid.uuid4())
        id = site.add_connection_to_current_page(Action.ActionType.CLICK, "[href='%s']" % url, 0)
        action = site.get_action({'connection': {'data': {'url': url}}, 'id': id})
        assert action._type == Action.ActionType.CLICK
        assert action.connection == id


    def test_update_current_page(self):
        from Site.Site import Site
        site = Site("http://%s.url/for/page" % uuid.uuid4())
        page1_id = str(uuid.uuid4())
        page1_content = str(uuid.uuid4())
        page2_id = str(uuid.uuid4())
        page2_content = str(uuid.uuid4())
        page3_content = str(uuid.uuid4())
        site._pages[page1_id] = page1_content
        site._pages[page2_id] = page2_content
        site._current = page1_id
        site.update_current_page(page3_content)
        assert site._pages[page1_id] == page3_content
        assert site._pages[page2_id] == page2_content
        assert site.get_current_page() == page3_content

    def test_on_path_finding(self):
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
        connection_1_data = {'css': str(uuid.uuid4()), 'nb': 0}
        connection_1_content = {'from': node_start, 'to': node_1, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': connection_1_data}
        connection_2_id = str(uuid.uuid4())
        connection_2_data = {'css': str(uuid.uuid4()), 'nb': 0}
        connection_2_content = {'from': node_1, 'to': node_2, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': connection_2_data}
        connection_3_id = str(uuid.uuid4())
        connection_3_data = {'css': str(uuid.uuid4()), 'nb': 0}
        connection_3_content = {'from': node_2, 'to': node_end, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': connection_3_data}
        connection_4_id = str(uuid.uuid4())
        connection_4_data = {'css': str(uuid.uuid4()), 'nb': 0}
        connection_4_content = {'from': node_2, 'to': node_1, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': connection_4_data}
        connection_5_id = str(uuid.uuid4())
        connection_5_data = {'css': str(uuid.uuid4()), 'nb': 0}
        connection_5_content = {'from': node_start, 'to': node_2, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': connection_5_data}
        connection_6_id = str(uuid.uuid4())
        connection_6_data = {'css': str(uuid.uuid4()), 'nb': 0}
        connection_6_content = {'from': node_end, 'to': None, 'explored': False, 'type': site.ConnectionTypes.LINK, 'data': connection_6_data}
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
        path = site.find_shortest_path(node_start, node_end)
        assert path[0] == {'connection': {'from': node_start, 'to': node_2, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': connection_5_data}, 'id': connection_5_id}
        assert path[1] == {'connection': {'from': node_2, 'to': node_end, 'explored': True, 'type': site.ConnectionTypes.LINK, 'data': connection_3_data}, 'id': connection_3_id}
        actions = site.get_actions_to(node_end)
        assert len(actions) == 2
        assert actions[0]._type == Action.ActionType.CLICK
        assert actions[0].connection == connection_5_id
        assert actions[1]._type == Action.ActionType.CLICK
        assert actions[1].connection == connection_3_id
        assert site.get_distance_to(connection_6_id) == 2
        actions = site.get_first_connection_unexplored()
        assert len(actions) == 3
        assert actions[0]._type == Action.ActionType.CLICK
        assert actions[0].connection == connection_5_id
        assert actions[1]._type == Action.ActionType.CLICK
        assert actions[1].connection == connection_3_id
        assert actions[2]._type == Action.ActionType.CLICK
        assert actions[2].connection == connection_6_id
        site._current = node_end
        actions = site.get_first_connection_unexplored()
        assert len(actions) == 1
        assert actions[0]._type == Action.ActionType.CLICK
        assert actions[0].connection == connection_6_id
        html = str('<html><body><div>new_page</div></body></html>')
        page = site.current_page(html, '', connection_6_id)
        assert site._pages[site.get_uniq_id(html, '')] == page
        assert site._connections[connection_6_id]['explored'] == True
        assert site._connections[connection_6_id]['to'] == site.get_uniq_id(html, '')
        actions = site.get_first_connection_unexplored()
        assert actions == None
        gexf = etree.Element('test')
        gexf_site = site.get_gexf()
        assert gexf_site.xpath('//meta/creator')[0].text == "Pallas"
        assert gexf_site.xpath('//meta/description')[0].text == site_url
        assert len(gexf_site.xpath('//nodes/node')) == 6
        assert len(gexf_site.xpath('//edges/edge')) == 7
