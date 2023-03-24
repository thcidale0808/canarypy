from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from canarypy.api.config import DBConfig


def get_sessionlocal():
    db_url = DBConfig().get_url()
    engine = create_engine(db_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
