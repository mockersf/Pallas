import logging

import browsermobproxy
from selenium import webdriver

from Main.singleton import singleton
from Main.Configuration import Configuration
from Site.Page import Page


@singleton
class Browser:
    _driver = None
    _proxy_server = None
    _proxy_client = None
    _site = None

    def __init__(self):
        pass

    def start(self, site):
        config = Configuration()
        #browsermobproxy_bin = "" if config.proxy_path is None else config.proxy_path
        #self._proxy_server = browsermobproxy.Server(browsermobproxy_bin + "browsermob-proxy")
        #self._proxy_server.start()
        #self._proxy_client = self._proxy_server.create_proxy()
        #profile = webdriver.FirefoxProfile()
        #profile.set_proxy(self._proxy_client.selenium_proxy())
        #self._driver = webdriver.Firefox(firefox_profile=profile)
        self._driver = webdriver.PhantomJS()
        self._site = site

    def stop(self):
        #self._proxy_server.stop()
        self._driver.quit()

    def add_remap_urls(self, urls):
        pass
        #import socket
        #for url in urls:
        #    self._proxy_client.remap_hosts(url, socket.gethostbyname(url))

    def setup(self, query):
        pass
        #self._proxy_client.new_har(query)

    def teardown(self, query, connection_id=None):
        logging.debug('browser is ready')
        #self._proxy_client.wait_for_traffic_to_stop(1000, 5000)
        logging.debug('no query ran for 1 second !')
        page = self._site.current_page(self._driver.page_source, self._driver.current_url, connection_id)
        #for entry in self._proxy_client.har['log']['entries']:
        #    logging.debug("%-4s %s - %s" %
        #                  (entry['request']['method'], entry['request']['url'], entry['response']['status']))
        #    page.add_call(entry)

    def get(self, url=None):
        self.setup('get')
        if url is None:
            logging.info('going to %s' % (self._site.url))
            self._driver.get(self._site.url)
        else:
            logging.info('going to %s' % (url))
            self._driver.get(url)
        self.teardown('get')

    def click(self, action):
        self.setup('click')
        logging.info('doing %s' % (action))
        logging.info('current page %s (%s)' % (self._site._current, self._site._pages[self._site._current]._url))
        try:
            action.data['find'](self._driver).click()
        except Exception as e:
            logging.warning('error clicking ' + str(e))
            raise
        self.teardown('click', action.connection)

    def study_state(self):
        page = self._site.get_current_page()
        try:
            elems = self._driver.find_elements_by_tag_name("input")
        except:
            elems = []
        for elem in elems:
            logging.debug('%s %s %s' % (elem.tag_name, elem.get_attribute('type'), elem.get_attribute('id')))
            page.add_interest({'type': 'input', 'obj': elem})
        try:
            links = self._driver.find_elements_by_tag_name("a")
        except:
            links = []
        for link in links:
            logging.debug('%s %s %s' % (link.tag_name, link.get_attribute('href'), link.get_attribute('id')))
            self._site.add_link(link.get_attribute('href'))
        self._site.update_current_page(page)
