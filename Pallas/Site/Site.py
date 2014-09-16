try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import hashlib
import logging
import uuid

from .Page import Page
from Main.Action import Action


class Site:
    _url = None
    _pages = None
    _connections = None
    _current = None

    class ConnecionTypes:
        LINK = "link"
        FORM = "form"

    def __init__(self, url):
        self._url = url
        self._pages = {}
        self._connections = {}

    def __repr__(self):
        return "<Site ('%s')" % (self._url)

    @property
    def url(self):
        return self._url

    @property
    def hostname(self):
        return urlparse(self._url).hostname

    def current_page(self, html_source, url, connection_id=None):
        uniq_page = hashlib.md5(html_source.encode('utf-8')).hexdigest()
        if self._current is not None:
            if connection_id is not None:
                connections = [id for id, connection in self._connections.items() if connection['from'] == self._current and id == connection_id]
                if len(connections) == 1:
                    self._connections[connections[0]]['explored'] = True
                    self._connections[connections[0]]['to'] = uniq_page
            else:
                connections = [id for id, connection in self._connections.items() if connection['from'] == self._current and connection['type'] == self.ConnecionTypes.LINK and connection['data']['url'] == url]
                if len(connections) == 1:
                    self._connections[connections[0]]['explored'] = True
                    self._connections[connections[0]]['to'] = uniq_page
        if uniq_page not in self._pages:
            self._pages[uniq_page] = Page(url)
        self._current = uniq_page
        return self._pages[uniq_page]

    def add_link(self, url):
        connections = [connection for connection in list(self._connections.values()) if connection['from'] == self._current and connection['type'] == self.ConnecionTypes.LINK and connection['data']['url'] == url]
        if len(connections) == 0:
            self._connections[uuid.uuid4()] = {'from': self._current, 'to': None, 'explored': False, 'type': self.ConnecionTypes.LINK, 'data': {'url': url}}

    def get_distance_to(self, connection_uuid):
        return len(self.get_actions_to(self._connections[connection_uuid]['from']))

    def get_actions_to(self, page):
        connections = self.find_shortest_path(self._current, page)
        actions = []
        for connection in connections:
            actions += [self.get_action(connection)]
        return actions

    def get_action(self, connection):
        xpath = "//a[contains(@href, '%s')]" % (connection['connection']['data']['url'][len(self._url):] if self._url in connection['connection']['data']['url'] else connection['connection']['data']['url'])
        return Action(type=Action.ActionType.CLICK, data={'xpath' : xpath, 'find' : lambda driver: driver.find_element_by_xpath(xpath)}, connection=connection['id'])

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
        links = [{'id': id, 'connection': elem} for id, elem in self._connections.items() if elem['from'] == self._current and not elem['explored'] and elem['type'] == self.ConnecionTypes.LINK]
        if len(links) > 0:
            return [self.get_action(links[0])]
        else:
            links = [{'id': id, 'connection':elem, 'dist': self.get_distance_to(id)} for id, elem in self._connections.items() if not elem['explored'] and elem['type'] == self.ConnecionTypes.LINK]
            if len(links) > 0:
                links = sorted(links, key=lambda item: item['dist'])
                return self.get_actions_to(links[0]['connection']['from']) + [self.get_action(links[0])]
            return None

    def update_current_page(self, page):
        self._pages[self._current] = page

    def show_graph(self):
        for page in self._pages:
            logging.info("'%s' -> '%s'" % (page, self._pages[page]))
            for id in [id for id in self._connections if self._connections[id]['from'] == page]:
                logging.info("'%s' -> '%s'" % (id, self._connections[id]))
