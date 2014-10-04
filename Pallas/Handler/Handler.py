import os
import json

from flask import Flask, send_from_directory, jsonify, request

from Main.Configuration import Configuration

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/start', methods=['POST'])
def start():
    tt = request.get_json()
    return json.dumps(tt)

@app.route('/default-target.json')
def default_target():
    config = Configuration()
    return jsonify(url=config.target, browser=None)

@app.route('/s/<path:filename>')
def send_file(filename):
    rootdir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(rootdir, 'ui'), filename)
