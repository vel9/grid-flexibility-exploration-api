from flask import Flask, request, jsonify
from database import db_session
from resource_data_service import insert_resource, delete_resource_by_id
from resource_service import get_resource_and_lowest_price_windows, get_resources_and_lowest_price_windows
from validator import validate_add_resource

app = Flask(__name__)


@app.route('/resources/view', methods=['GET'])
def get_resources():
    """
    Get price data and lowest windows within it for each resource

    :return: list of resources and chart data
    """
    return get_resources_and_lowest_price_windows(), 200


@app.route('/resource/view/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    """
    Get price data and resource's lowest price windows

    :param resource_id: resource unique id
    :return: resource and chart data
    """
    return get_resource_and_lowest_price_windows(resource_id), 200


@app.route('/resource/add', methods=['POST'])
def add_resource():
    """
    validate params and insert new resource in data store

    :return: success if inserted
    """
    name = request.form['name']
    hours = request.form['hours']
    result = validate_add_resource(name, hours)
    if result.has_errors:
        return vars(result)

    insert_resource(name, int(hours))
    return jsonify(success=True)


@app.route('/resource/delete', methods=['POST'])
def delete_resource():
    """
    delete resource from data store by id

    :return: success if deleted
    """
    id_to_delete = request.form['unique_id']
    delete_resource_by_id(id_to_delete)
    return jsonify(success=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
