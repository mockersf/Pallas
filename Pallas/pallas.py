import logging

from Main.Configuration import Configuration
from Main.Browser import Browser
from Site.Site import Site
from Handler.Handler import app



def check_website(url):
    config = Configuration()
    site = Site(url)

    browser = Browser()
    browser.start(site)

    # strange behaviour from browsermob proxy, dsn doesn't always work
    browser.add_remap_urls([site.hostname])

    browser.get()
    browser.study_state()
    actions = site.get_first_connection_unexplored()
    while actions is not None:
        logging.info('%s action(s) needed to reach this connection' % (len(actions)))
        for action in actions:
            action.do()
        browser.study_state()
        actions = site.get_first_connection_unexplored()
    site.show_graph()
    browser.stop()

if __name__ == '__main__':
    config = Configuration()
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=config.get_log_level())
    if config.auto:
        check_website(config.target)
    else:
        app.run(host="0.0.0.0")
