import pytest
from sqlalchemy import func
from experts_dw import db, models

@pytest.fixture
def session():
  with db.session('hotel') as session:
    yield session

def test_pub(session):
  count = session.query(func.count(models.Pub.uuid)).scalar()
  assert count > 0

def test_views(session):
  count = session.query(func.count(models.AffiliateJobs.emplid)).scalar()
  assert count > 0
