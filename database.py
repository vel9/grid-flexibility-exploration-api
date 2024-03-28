from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# ref: https://flask.palletsprojects.com/en/3.0.x/patterns/sqlalchemy/
engine = create_engine('sqlite:///localdb/electrify-local.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    Initiate sqlite3 database connector
    """
    import models
    Base.metadata.create_all(bind=engine)
