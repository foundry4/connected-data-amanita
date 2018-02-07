import base64
import json
import logging
import os

from flask import current_app, Flask, render_template, request, jsonify

from domain import root, content, items, search

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # should this return the schema?
    res = root.obj
    return jsonify(res)

@app.route('/content', methods=['GET'])
def get_content():
    res = content.obj
    return jsonify(res)

@app.route('/items', methods=['GET'])
def get_items():
    res = items.multi_obj
    return jsonify(res), 200

@app.route('/items/<string:item>', methods=['GET'])
def get_item(item):
    res = {item: items.single_obj}
    return jsonify(res), 200


@app.route('/items/<string:item>', methods=['DELETE'])
def del_item(item):
    return jsonify({'deleted':item}),200

@app.route('/items', methods=['POST'])
def post_item():
    return jsonify({'added':request.form}),200

@app.route('/items/<path:item>', methods=['PATCH'])
def patch_item(item):
    return jsonify({'patched':item}),200

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """Uh oh!""".format(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.testing = True
    # test = app.test_client()
    # r = test.get('/content')
    # pass
