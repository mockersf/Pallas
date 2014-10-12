import os
import json
import logging

from lxml import etree
from flask import Flask, send_from_directory, jsonify, request

from Main.Configuration import Configuration
from Main.Browser import Browser
from Site.Site import Site
from Main.Action import Action


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
    return etree.tostring(site.get_gexf())

@app.route('/add_connection_and_go', methods=['POST'])
def add_connection_and_go():
    connection = request.get_json()
    logging.info('%s - %s' % (connection['css'], connection['nb']))
    site = Site()
    connection_id = site.add_connection_to_current_page(Action.ActionType.CLICK, connection['css'], connection['nb'])
    action = site.get_action_from_id(connection_id)
    action.do()
    return etree.tostring(site.get_gexf())

@app.route('/default-target.json')
def default_target():
    config = Configuration()
    return jsonify(url=config.target, browser=config.browser, proxy=config.proxy_path)

@app.route('/details/<node>.json')
def node_details(node):
    config = Configuration()
    site = Site()
    page = site._pages[node]
    return jsonify(url=page.url, html=page.html_source)

@app.route('/s/<path:filename>')
def send_file(filename):
    rootdir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(rootdir, 'ui'), filename)
