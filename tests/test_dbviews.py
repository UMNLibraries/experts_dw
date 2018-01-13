from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from experts_dw import db, dbviews
from experts_dw.models import PureEligibleAffJob, PureEligibleEmpJob
from sqlalchemy import func
from sqlalchemy.engine import ResultProxy

session = db.session('hotel')

def test_pure_eligible_affiliate():
  result = dbviews.create_pure_eligible_affiliate()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_employee():
  result = dbviews.create_pure_eligible_employee()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_demog():
  result = dbviews.create_pure_eligible_demog()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_person():
  result = dbviews.create_pure_eligible_person()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_aff_job():
  result = dbviews.create_pure_eligible_aff_job()
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleAffJob.emplid)).scalar()
  assert rows > 0

def test_pure_eligible_emp_job():
  result = dbviews.create_pure_eligible_emp_job()
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleEmpJob.emplid)).scalar()
  assert rows > 0
