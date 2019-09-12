import pytest
from sqlalchemy import func
from sqlalchemy.engine import ResultProxy
from experts_dw import db, dbviews, models
from experts_dw.models import PureEligibleDemographics, PureEligiblePerson, PureEligibleAffiliateJob, PureEligibleEmployeeJob

@pytest.fixture
def session():
  with db.session('hotel') as session:
    yield session

def test_list_view_creation_methods():
  assert len(dbviews._view_creation_methods()) > 0

# Create all views
def test_create_all_views(session):
  results = dbviews.create_all_views(session)
  for fn in dbviews._view_creation_methods():
    assert isinstance(results[fn], ResultProxy)

# Verify views with backing models return rows
def test_view_rows(session):
  for v in [
      PureEligibleDemographics,
      PureEligiblePerson,
      PureEligibleAffiliateJob,
      PureEligibleEmployeeJob
  ]:
    rows = session.query(func.count(v.emplid)).scalar()
    assert rows > 0
