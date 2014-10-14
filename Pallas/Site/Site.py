try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import hashlib
import logging
import uuid

from .Page import Page
from Main.Action import Action

from Main.singleton import singleton


@singleton
class Site:
    _url = None
    _pages = None
    _connections = None
    _current = None

    class ConnectionTypes:
        LINK = "link"
        START = "start"
        FORM = "form"

    def __init__(self, url):
        self._url = url
        self._pages = {}
        self._connections = {}

    def __repr__(self):
        return "<Site ('%s')>" % (self._url)

    @property
    def url(self):
        return self._url

    @property
    def current(self):
        return self._current

    @property
    def hostname(self):
        return urlparse(self._url).hostname

    def get_uniq_id(self, html_source, url):
        return hashlib.md5(html_source.encode('utf-8')).hexdigest()

    def current_page(self, html_source, url, connection_id=None):
        uniq_page = self.get_uniq_id(html_source, url)
        if connection_id is not None:
            connections = [id for id, connection in self._connections.items() if connection['from'] == self._current and id == connection_id]
            if len(connections) == 1:
                self._connections[connections[0]]['explored'] = True
                self._connections[connections[0]]['to'] = uniq_page
        else:
            self._connections[uuid.uuid4()] = {'from': "start", 'to': uniq_page, 'explored': True, 'type': self.ConnectionTypes.START, 'data': {'url': url}}
        if uniq_page not in self._pages:
            self._pages[uniq_page] = Page(url, html_source)
        self._current = uniq_page
        return self._pages[uniq_page]

    def add_link(self, url):
        connections = [connection for connection in list(self._connections.values()) if connection['from'] == self._current and connection['type'] == self.ConnectionTypes.LINK and connection['data']['url'] == url]
        if len(connections) == 0:
            self._connections[uuid.uuid4()] = {'from': self._current, 'to': None, 'explored': False, 'type': self.ConnectionTypes.LINK, 'data': {'url': url}}

    def get_distance_to(self, connection_uuid):
        return len(self.get_actions_to(self._connections[connection_uuid]['from']))

    def get_actions_to(self, page):
        connections = self.find_shortest_path(self._current, page)
        actions = []
        for connection in connections:
            actions += [self.get_action(connection)]
        return actions

    def get_action(self, connection):
        return self.get_action_from_id(connection['id'])

    def get_action_from_id(self, connection_id):
        connection = self._connections[connection_id]
        if 'url' in connection['data']:
            xpath = "//a[contains(@href, '%s')]" % (connection['data']['url'][len(self._url):] if self._url in connection['data']['url'] else connection['data']['url'])
            return Action(type=Action.ActionType.CLICK, data={'xpath' : xpath, 'find' : lambda driver: driver.find_element_by_xpath(xpath)}, connection=connection_id)
        if 'css' in connection['data']:
            css = connection['data']['css']
            nb = connection['data']['nb']
            return Action(type=Action.ActionType.CLICK, data={'find' : lambda driver: driver.find_elements_by_css_selector(css)[nb]}, connection=connection_id)

    def find_shortest_path(self, start, end, path=[]):
        if start == end:
            return path
        shortest = None
        for connection_id in [{'id': id, 'connection': connection} for id, connection in self._connections.items() if connection['from'] == start]:
            if connection_id['connection']['to'] is not None and connection_id['connection']['to'] not in [connection['connection']['to'] for connection in path]:
                newpath = self.find_shortest_path(connection_id['connection']['to'], end, path + [connection_id])
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def get_first_connection_unexplored(self):
        links = [{'id': id, 'connection': elem} for id, elem in self._connections.items() if elem['from'] == self._current and not elem['explored'] and elem['type'] == self.ConnectionTypes.LINK]
        if len(links) > 0:
            return [self.get_action(links[0])]
        else:
            try:
                links = [{'id': id, 'connection':elem, 'dist': self.get_distance_to(id)} for id, elem in self._connections.items() if not elem['explored'] and elem['type'] == self.ConnectionTypes.LINK]
            except TypeError:
                logging.info("Dead end on page '%s'" % (self._current))
                return None
            if len(links) > 0:
                links = sorted(links, key=lambda item: item['dist'])
                return self.get_actions_to(links[0]['connection']['from']) + [self.get_action(links[0])]
            return None

    def update_current_page(self, page):
        self._pages[self._current] = page

    def get_current_page(self):
        return self._pages[self._current]

    def add_connection_to_current_page(self, connection_type, css, nb):
        id = uuid.uuid4()
        self._connections[id] = {'from': self._current, 'to': None, 'explored': False, 'type': connection_type, 'data': {'css': css, 'nb': nb}}
        return id

    def show_graph(self):
        logging.info("start")
        for id in [id for id in self._connections if self._connections[id]['from'] == "start"]:
            logging.info("'%s' -> '%s'" % (id, self._connections[id]))
        for page in self._pages:
            logging.info("'%s' -> '%s'" % (page, self._pages[page]))
            for id in [id for id in self._connections if self._connections[id]['from'] == page]:
                logging.info("'%s' -> '%s'" % (id, self._connections[id]))

    def get_gexf(self):
        from gexf import Gexf
        gexf = Gexf("Pallas", self.url)
        graph = gexf.addGraph("directed", "static", "Current site exploration")
        graph.addNode('start', 'start')
        for page in self._pages:
          graph.addNode(page, self._pages[page]._url)
        for id in [id for id in self._connections if self._connections[id]['from'] == "start"]:
          graph.addEdge(id, "start", self._connections[id]['to'])
        for page in self._pages:
            for id in [id for id in self._connections if self._connections[id]['from'] == page and self._connections[id]['explored']]:
              graph.addEdge(id, self._connections[id]['from'], self._connections[id]['to'])
        return gexf.getXML()
