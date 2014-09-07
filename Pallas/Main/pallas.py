import logging

from Configuration import Configuration
from Browser import Browser

config = Configuration()
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=config.get_log_level())

url = 'github.com'

browser = Browser()
browser.start()
#strange behaviour from browsermob proxy, dsn doesn't always work
browser.add_remap_urls([url])
browser.get('http://' + url)
browser.study_state()
browser.stop()