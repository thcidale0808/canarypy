from sqlalchemy.orm import Session

from canarypy.api.db.base import get_sessionlocal


def get_db() -> Session:
    """Creates a local DB session object.

    :return: DB session object
    """
    Session = get_sessionlocal()
    db = Session()
    try:
        yield db
    finally:
        db.close()
