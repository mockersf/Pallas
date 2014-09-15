import logging

from Main.Configuration import Configuration
from Main.Browser import Browser
from Site.Site import Site

config = Configuration()
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=config.get_log_level())

url = config.target
site = Site(url)

browser = Browser()
browser.start(site)
# strange behaviour from browsermob proxy, dsn doesn't always work
browser.add_remap_urls([site.hostname])
browser.get()
browser.study_state()
for link in [elem['target'] for hash, page in site._pages.items()
             for elem in page._interests if elem['type'] == 'link']:
    logging.info(link)
    browser.get(link)
browser.stop()
