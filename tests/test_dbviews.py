import pytest
from sqlalchemy import func
from sqlalchemy.engine.cursor import CursorResult
from experts_dw import db, dbviews
from experts_dw.models import PureEligibleDemographics, PureEligiblePerson, PureEligibleAffiliateJob, PureEligibleEmployeeJob, PureEligiblePOIJob

@pytest.fixture
def session():
  with db.session('hotel') as session:
    yield session

def test_list_view_creation_functions():
  assert len(dbviews._view_creation_functions()) > 0

# Create all views
def test_create_all_views(session):
  results = dbviews.create_all_views(session)
  for fn in dbviews._view_creation_functions():
    assert isinstance(results[fn], CursorResult)

# Verify views with backing models return rows
def test_view_rows(session):
  for v in [
      PureEligibleDemographics,
      PureEligiblePerson,
      PureEligibleAffiliateJob,
      PureEligibleEmployeeJob,
      PureEligiblePOIJob,
  ]:
    rows = session.query(func.count(v.emplid)).scalar()
    assert rows > 0
