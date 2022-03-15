from contextlib import contextmanager
import cx_Oracle
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_mptt import mptt_sessionmaker

# If a path to the Oracle client libraries was defined, pass to cx_Oracle with init method
oracle_libs_path = os.environ.get('ORACLE_CLIENT_LIBRARIES_PATH')
if oracle_libs_path:
     cx_Oracle.init_oracle_client(lib_dir=oracle_libs_path)

default_db_name = 'hotel'

def url(db_name=default_db_name):
    # db_name must be the generic part of the service name,
    # without the (tst|prd).oit suffix, e.g. 'dwe' or 'hotel'.
    url = 'oracle+cx_oracle://{}:"{}"@{}:{}/?service_name={}'.format(
        os.environ.get('EXPERTS_DB_USER'),
        os.environ.get('EXPERTS_DB_PASS'),
        os.environ.get('EXPERTS_DB_HOSTNAME'),
        os.environ.get('EXPERTS_DB_PORT'),
        os.environ.get('EXPERTS_DB_SERVICE_NAME'),
    )
    return url

def engine(db_name=default_db_name):
    return create_engine(
        url(db_name),
        max_identifier_length=128
    )

@contextmanager
def cx_oracle_connection():
    # Note that this approach to making a connection should not
    # require a tnsnames.ora config file.
    yield cx_Oracle.connect(
        os.environ.get('EXPERTS_DB_USER'),
        os.environ.get('EXPERTS_DB_PASS'),
        f'{os.environ.get("EXPERTS_DB_HOSTNAME")}:{os.environ.get("EXPERTS_DB_PORT")}/{os.environ.get("EXPERTS_DB_SERVICE_NAME")}',
        encoding='UTF-8'
    )

@contextmanager
def session(db_name=default_db_name):
    # Original:
    #Session = sessionmaker()
    # mptt docs:
    #Session = mptt_sessionmaker(sessionmaker(bind=engine))
    # This didn't work:
    #Session = mptt_sessionmaker(sessionmaker())

    Session = mptt_sessionmaker(sessionmaker(bind=engine(db_name)))
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
