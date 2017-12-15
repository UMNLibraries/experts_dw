from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from sqlalchemy import func
from experts_dw import db, models

session = db.session('hotel')

def test_pub():
  count = session.query(func.count(models.Pub.uuid)).scalar()
  assert count > 0

def test_views():
  count = session.query(func.count(models.AffiliateJobs.emplid)).scalar()
  assert count > 0
