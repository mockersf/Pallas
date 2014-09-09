import logging
from urlparse import urlparse

from Main.Configuration import Configuration
from Main.Browser import Browser

config = Configuration()
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=config.get_log_level())

url = config.target

browser = Browser()
browser.start()
#strange behaviour from browsermob proxy, dsn doesn't always work
browser.add_remap_urls([urlparse(url).hostname])
browser.get(url)
browser.study_state()
browser.stop()