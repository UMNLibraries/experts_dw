from experts_dw import db
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine
from experts_dw.models import PureJsonCollectionMeta

def test_engine():
  engine = db.engine('hotel')
  assert isinstance(engine, Engine)

def test_engine_with_no_args():
  engine = db.engine()
  assert isinstance(engine, Engine)

def test_session():
  with db.session('hotel') as session:
    assert isinstance(session, Session)

def test_session_with_no_args():
  with db.session() as session:
    assert isinstance(session, Session)
    # Exectue a statement to test that we can connect to the db
    # and get results:
    metadata = session.query(PureJsonCollectionMeta).all()
    assert metadata

def test_oracle_cx_connect_query():
    with db.cx_oracle_connection() as connection:
        # Execute sql to test that we have a connection and get results
        cur = connection.cursor()
        result = cur.execute(
            "SELECT COUNT(*) FROM UMN_DEPT_PURE_ORG"
        )
        assert result
