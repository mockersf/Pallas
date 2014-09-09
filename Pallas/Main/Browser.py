import logging

import browsermobproxy
from selenium import webdriver

from Main.Configuration import Configuration

class Browser:
    _driver = None
    _proxy_server = None
    _proxy_client = None
    
    def __init__(self):
        pass
    
    def start(self):
        config = Configuration()
        browsermobproxy_bin = "" if config.proxy_path is None else config.proxy_path
        self._proxy_server = browsermobproxy.Server(browsermobproxy_bin + "browsermob-proxy")
        self._proxy_server.start()
        self._proxy_client = self._proxy_server.create_proxy()
        profile  = webdriver.FirefoxProfile()
        profile.set_proxy(self._proxy_client.selenium_proxy())
        self._driver = webdriver.Firefox(firefox_profile=profile)
    
    def stop(self):
        self._proxy_server.stop()
        self._driver.quit()

    def add_remap_urls(self, urls):
        import socket
        for url in urls:
            self._proxy_client.remap_hosts(url, socket.gethostbyname(url))

    def setup(self, query):
        self._proxy_client.new_har(query)
    
    def teardown(self, query):
        for entry in self._proxy_client.har['log']['entries']:
            logging.debug("%-4s %s - %s" % (entry['request']['method'], entry['request']['url'], entry['response']['status']))

    def get(self, url):
        self.setup('get')
        self._driver.get(url)
        logging.debug('browser is ready')
        self._proxy_client.wait_for_traffic_to_stop(1000, 5000)
        logging.debug('no query ran for 1 second !')
        self.teardown('get')

    def study_state(self):
        try:
            elems = self._driver.find_elements_by_tag_name("input")
        except:
            elems = []
        for elem in elems:
            logging.debug('%s %s %s' % (elem.tag_name, elem.get_attribute('type'), elem.get_attribute('id')))
