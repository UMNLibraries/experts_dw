import pytest
from sqlalchemy import func
from sqlalchemy.engine import ResultProxy
from experts_dw import db, dbviews
from experts_dw.models import PureEligibleDemographics, PureEligiblePerson, PureEligibleAffiliateJob, PureEligibleEmployeeJob

@pytest.fixture
def session():
  with db.session('hotel') as session:
    yield session

def test_pure_eligible_affiliate(session):
  result = dbviews.create_pure_eligible_affiliate(session)
  assert isinstance(result, ResultProxy)

def test_pure_eligible_employee(session):
  result = dbviews.create_pure_eligible_employee(session)
  assert isinstance(result, ResultProxy)

def test_pure_eligible_demographics(session):
  result = dbviews.create_pure_eligible_demographics(session)
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleDemographics.emplid)).scalar()
  assert rows > 0

def test_pure_eligible_person(session):
  result = dbviews.create_pure_eligible_person(session)
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligiblePerson.emplid)).scalar()
  assert rows > 0

def test_pure_eligible_affiliate_job(session):
  result = dbviews.create_pure_eligible_affiliate_job(session)
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleAffiliateJob.emplid)).scalar()
  assert rows > 0

def test_pure_eligible_employee_job(session):
  result = dbviews.create_pure_eligible_employee_job(session)
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleEmployeeJob.emplid)).scalar()
  assert rows > 0
