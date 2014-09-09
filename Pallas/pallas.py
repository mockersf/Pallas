import logging

from Main.Configuration import Configuration
from Main.Browser import Browser
from Site.Site import Site

config = Configuration()
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=config.get_log_level())

url = config.target
site = Site(url)

browser = Browser()
browser.start()
#strange behaviour from browsermob proxy, dsn doesn't always work
browser.add_remap_urls([site.hostname])
browser.get(site.url)
browser.study_state()
browser.stop()