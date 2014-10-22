import os
import json
import logging

from lxml import etree
from flask import Flask, send_from_directory, jsonify, request, abort

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
    return jsonify(gexf=etree.tostring(site.get_gexf()).decode('utf-8'), current_page=site.current)

@app.route('/add_connection_and_go', methods=['POST'])
def add_connection_and_go():
    connection = request.get_json()
    logging.info('%s - %s' % (connection['css'], connection['nb']))
    site = Site()
    connection_id = site.add_connection_to_current_page(Action.ActionType.CLICK, connection['css'], connection['nb'])
    action = site.get_action_from_id(connection_id)
    action.do()
    return jsonify(gexf=etree.tostring(site.get_gexf()).decode('utf-8'), current_page=site.current)

@app.route('/follow_existing_connections', methods=['POST'])
def follow_existing_connections():
    infos = request.get_json()
    logging.info('%s' % (infos['target']))
    site = Site()
    actions = site.get_actions_to(infos['target'])
    for action in actions:
        action.do()
    return jsonify(gexf=etree.tostring(site.get_gexf()).decode('utf-8'), current_page=site.current)

@app.route('/back_to_start.json', methods=['GET'])
def back_to_start():
    logging.info('getting back to start point')
    site = Site()
    browser = Browser()
    browser.get()
    return jsonify(gexf=etree.tostring(site.get_gexf()).decode('utf-8'), current_page=site.current)

@app.route('/default-target.json')
def default_target():
    config = Configuration()
    return jsonify(url=config.target, browser=config.browser, proxy=config.proxy_path)

@app.route('/details/<node>.json')
def node_details(node):
    config = Configuration()
    site = Site()
    if not node in site._pages:
        abort(404)
    page = site._pages[node]
    has_path = site.get_actions_to(node) is not None
    return jsonify(url=page.url, html=page.html_source, has_path=has_path, connections=site.get_actions_from_page(node))

@app.route('/follow/<connection>.json')
def follow(connection):
    config = Configuration()
    site = Site()
    if not connection in site._connections:
        abort(404)
    if site._connections[connection]['from'] != site.current:
        abort(500)
    action = site.get_action_from_id(connection)
    action.do()
    return jsonify(gexf=etree.tostring(site.get_gexf()).decode('utf-8'), current_page=site.current)

@app.route('/s/<path:filename>')
def send_file(filename):
    rootdir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(rootdir, 'ui'), filename)
