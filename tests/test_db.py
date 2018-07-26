from experts_dw import db
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine

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
