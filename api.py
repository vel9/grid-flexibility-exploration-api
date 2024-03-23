from flask import Flask, request
from database import db_session
from resource_service import get_planned_resources, get_all_resources_as_dict, delete_resource_from_db, \
    add_resource_to_db, get_all_resource

app = Flask(__name__)


@app.route('/resources/view', methods=['GET'])
def get_resources():
    chart, table_data, grid_query = get_planned_resources()
    return {
        "resources": get_all_resources_as_dict(),
        "chart": chart,
        "table": table_data,
        "query": grid_query
    }, 200


@app.route('/resource/view/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    return get_all_resource(resource_id), 200


@app.route('/resource/add', methods=['POST'])
def add_resource():
    name = request.form['name']
    hours = request.form['hours']
    add_resource_to_db(name, int(hours))
    return 200


@app.route('/resource/delete', methods=['POST'])
def delete_resource():
    id_to_delete = request.form['unique_id']
    delete_resource_from_db(id_to_delete)
    return 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
