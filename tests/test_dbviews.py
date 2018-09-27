import pytest
from sqlalchemy import func
from sqlalchemy.engine import ResultProxy
from experts_dw import db, dbviews
from experts_dw.models import PureEligibleDemog, PureEligiblePerson, PureEligibleAffJob, PureEligibleEmpJob

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

def test_pure_eligible_demog(session):
  result = dbviews.create_pure_eligible_demog(session)
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleDemog.emplid)).scalar()
  assert rows > 0

def test_pure_eligible_person(session):
  result = dbviews.create_pure_eligible_person(session)
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligiblePerson.emplid)).scalar()
  assert rows > 0

def test_pure_eligible_aff_job(session):
  result = dbviews.create_pure_eligible_aff_job(session)
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleAffJob.emplid)).scalar()
  assert rows > 0

def test_pure_eligible_emp_job(session):
  result = dbviews.create_pure_eligible_emp_job(session)
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleEmpJob.emplid)).scalar()
  assert rows > 0
