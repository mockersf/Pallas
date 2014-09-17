import os.path
import sys
import uuid

def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class Test_Site_Site(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_getting_hostname(self):
        from Site.Site import Site
        host = '%s.url' % uuid.uuid4()
        site = Site('http://%s/' % host)
        assert site.hostname == host

    def test_adding_one_page(self):
        from Site.Site import Site
        site = Site('http://google.com/')
        assert len(site._pages) == 0
        site.current_page("<html></html>", 'http://google.com/')
        assert len(site._pages) == 1

    def test_adding_two_page(self):
        from Site.Site import Site
        site = Site('http://google.com/')
        assert len(site._pages) == 0
        site.current_page("<html></html>", 'http://google.com/')
        site.current_page("<html><body></body></html>", 'http://google.com/2')
        assert len(site._pages) == 2

    def test_adding_same_page_twice(self):
        from Site.Site import Site
        site = Site('http://google.com/')
        assert len(site._pages) == 0
        site.current_page("<html></html>", 'http://google.com/')
        site.current_page("<html></html>", 'http://google.com/')
        assert len(site._pages) == 1

    def test_repr_getter(self):
        from Site.Site import Site
        url = "http://%s.url/for/page" % uuid.uuid4()
        site = Site(url)
        assert site.__repr__() == ("<Site ('%s')>" % (url))
        assert site.url == url

    def test_add_link(self):
        from Site.Site import Site
        url = "http://test.url/for/page"
        site = Site(url)
        current_page = uuid.uuid4()
        site._current = current_page
        url = 'http://test.com/about.html'
        connection1 = {'from': current_page, 'type': Site.ConnecionTypes.LINK, 'explored': False, 'to': None, 'data': {'url': url}}
        site.add_link(url)
        assert len(site._connections) == 1
        assert site._connections.values()[0] == connection1
        site.add_link(url)
        assert len(site._connections) == 1

    def test_get_action(self):
        from Site.Site import Site
        from Main.Action import Action
        site_url = "http://test.url/for/page"
        site = Site(site_url)
        url = str(uuid.uuid4())
        id = str(uuid.uuid4())
        action = site.get_action({'connection': {'data': {'url': url}}, 'id': id})
        assert action._type == Action.ActionType.CLICK
        assert action.connection == id
        assert action.data['xpath'] == "//a[contains(@href, '%s')]" % url
        url = str(uuid.uuid4())
        id = str(uuid.uuid4())
        action = site.get_action({'connection': {'data': {'url': site_url + url}}, 'id': id})
        assert action._type == Action.ActionType.CLICK
        assert action.connection == id
        assert action.data['xpath'] == "//a[contains(@href, '%s')]" % url


    def test_update_current_page(self):
        from Site.Site import Site
        site = Site("http://test.url/for/page")
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

    def test_on_path_finding(self):
        from Site.Site import Site
        from Main.Action import Action
        site = Site("http://test.url/for/page")
        node_start = str(uuid.uuid4())
        node_1 = str(uuid.uuid4())
        node_2 = str(uuid.uuid4())
        node_end = str(uuid.uuid4())
        connection_1_id = str(uuid.uuid4())
        connection_1_url = str(uuid.uuid4())
        connection_1_content = {'from': node_start, 'to': node_1, 'explored': True, 'type': site.ConnecionTypes.LINK, 'data': {'url': connection_1_url}}
        connection_2_id = str(uuid.uuid4())
        connection_2_url = str(uuid.uuid4())
        connection_2_content = {'from': node_1, 'to': node_2, 'explored': True, 'type': site.ConnecionTypes.LINK, 'data': {'url': connection_2_url}}
        connection_3_id = str(uuid.uuid4())
        connection_3_url = str(uuid.uuid4())
        connection_3_content = {'from': node_2, 'to': node_end, 'explored': True, 'type': site.ConnecionTypes.LINK, 'data': {'url': connection_3_url}}
        connection_4_id = str(uuid.uuid4())
        connection_4_url = str(uuid.uuid4())
        connection_4_content = {'from': node_2, 'to': node_1, 'explored': True, 'type': site.ConnecionTypes.LINK, 'data': {'url': connection_4_url}}
        connection_5_id = str(uuid.uuid4())
        connection_5_url = str(uuid.uuid4())
        connection_5_content = {'from': node_start, 'to': node_2, 'explored': True, 'type': site.ConnecionTypes.LINK, 'data': {'url': connection_5_url}}
        connection_6_id = str(uuid.uuid4())
        connection_6_url = str(uuid.uuid4())
        connection_6_content = {'from': node_end, 'to': None, 'explored': False, 'type': site.ConnecionTypes.LINK, 'data': {'url': connection_6_url}}
        site._connections[connection_1_id] = connection_1_content
        site._connections[connection_2_id] = connection_2_content
        site._connections[connection_3_id] = connection_3_content
        site._connections[connection_4_id] = connection_4_content
        site._connections[connection_5_id] = connection_5_content
        site._connections[connection_6_id] = connection_6_content
        site._current = node_start
        path = site.find_shortest_path(node_start, node_end)
        assert path[0] == {'connection': {'from': node_start, 'to': node_2, 'explored': True, 'type': site.ConnecionTypes.LINK, 'data': {'url': connection_5_url}}, 'id': connection_5_id}
        assert path[1] == {'connection': {'from': node_2, 'to': node_end, 'explored': True, 'type': site.ConnecionTypes.LINK, 'data': {'url': connection_3_url}}, 'id': connection_3_id}
        actions = site.get_actions_to(node_end)
        assert len(actions) == 2
        assert actions[0]._type == Action.ActionType.CLICK
        assert actions[0].connection == connection_5_id
        assert actions[0].data['xpath'] == "//a[contains(@href, '%s')]" % connection_5_url
        assert actions[1]._type == Action.ActionType.CLICK
        assert actions[1].connection == connection_3_id
        assert actions[1].data['xpath'] == "//a[contains(@href, '%s')]" % connection_3_url
        assert site.get_distance_to(connection_6_id) == 2
        actions = site.get_first_connection_unexplored()
        assert len(actions) == 3
        assert actions[0]._type == Action.ActionType.CLICK
        assert actions[0].connection == connection_5_id
        assert actions[0].data['xpath'] == "//a[contains(@href, '%s')]" % connection_5_url
        assert actions[1]._type == Action.ActionType.CLICK
        assert actions[1].connection == connection_3_id
        assert actions[1].data['xpath'] == "//a[contains(@href, '%s')]" % connection_3_url
        assert actions[2]._type == Action.ActionType.CLICK
        assert actions[2].connection == connection_6_id
        assert actions[2].data['xpath'] == "//a[contains(@href, '%s')]" % connection_6_url
        site._current = node_end
        actions = site.get_first_connection_unexplored()
        assert len(actions) == 1
        assert actions[0]._type == Action.ActionType.CLICK
        assert actions[0].connection == connection_6_id
        assert actions[0].data['xpath'] == "//a[contains(@href, '%s')]" % connection_6_url
