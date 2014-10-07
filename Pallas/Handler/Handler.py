import os
import json
import logging

from lxml import etree
from flask import Flask, send_from_directory, jsonify, request

from Main.Configuration import Configuration
from Main.Browser import Browser
from Site.Site import Site

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/start', methods=['POST'])
def start():
    starter = request.get_json()
    Configuration().browser = starter['browser']
    if starter['proxy'] == 'no proxy':
        Configuration().proxy_path = None
    else:
        Configuration().proxy_path = starter['proxy_path']
    site = Site(starter['url'])
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
    return etree.tostring(site.get_gexf())

@app.route('/default-target.json')
def default_target():
    config = Configuration()
    return jsonify(url=config.target, browser=config.browser, proxy=config.proxy_path)

@app.route('/s/<path:filename>')
def send_file(filename):
    rootdir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(rootdir, 'ui'), filename)
