from flask import Flask, request, jsonify
from database import db_session
from resource_data_service import insert_resource, delete_resource_by_id
from resource_service import get_resource_with_lowest_price_windows, get_resources_with_lowest_price_windows

app = Flask(__name__)


@app.route('/resources/view', methods=['GET'])
def get_resources():
    return get_resources_with_lowest_price_windows(), 200


@app.route('/resource/view/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    return get_resource_with_lowest_price_windows(resource_id), 200


@app.route('/resource/add', methods=['POST'])
def add_resource():
    name = request.form['name']
    hours = request.form['hours']
    insert_resource(name, int(hours))
    return jsonify(success=True)


@app.route('/resource/delete', methods=['POST'])
def delete_resource():
    id_to_delete = request.form['unique_id']
    delete_resource_by_id(id_to_delete)
    return jsonify(success=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
