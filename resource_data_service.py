import uuid

from database import init_db, db_session
from models import Resource


def query_all_resources():
    init_db()
    return Resource.query.all()


def query_resource_by_id(resource_id: str):
    return Resource.query.get(resource_id)


def insert_resource(name: str, hours: int):
    resource = Resource(str(uuid.uuid4()), name, hours)
    db_session.add(resource)
    db_session.commit()


def delete_resource_by_id(id_to_delete: str):
    Resource.query.filter_by(unique_id=id_to_delete).delete()
    db_session.commit()
