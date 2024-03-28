import uuid

from database import init_db, db_session
from models import Resource


def query_all_resources():
    """
    Get all resources from database

    :return: list of resources
    """
    init_db()
    return Resource.query.all()


def query_resource_by_id(resource_id: str):
    """
    Get resource by id from database

    ref: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#querying

    :param resource_id: resource unique id
    :return: found resource object
    """
    return Resource.query.get(resource_id)


def insert_resource(name: str, hours: int):
    """
    Add resource to database

    :param name: resource name
    :param hours: number of hours for resource
    """
    resource = Resource(str(uuid.uuid4()), name, hours)
    db_session.add(resource)
    db_session.commit()


def delete_resource_by_id(id_to_delete: str):
    """
    Hard delete resource from database

    ref: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#deleting

    :param id_to_delete: resource unique id
    """
    Resource.query.filter_by(unique_id=id_to_delete).delete()
    db_session.commit()
