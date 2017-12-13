from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from experts_dw import db
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine

def test_engine():
  engine = db.engine('hotel')
  assert isinstance(engine, Engine)

def test_session():
  session = db.session('hotel')
  assert isinstance(session, Session)
