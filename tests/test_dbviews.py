from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from experts_dw import db, dbviews
from experts_dw.models import PureEligibleEmployeeJob
from sqlalchemy import func
from sqlalchemy.engine import ResultProxy

session = db.session('hotel')

def test_pure_eligible_affiliate():
  result = dbviews.create_pure_eligible_affiliate()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_employee():
  result = dbviews.create_pure_eligible_employee()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_person():
  result = dbviews.create_pure_eligible_person()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_employee_job():
  result = dbviews.create_pure_eligible_employee_job()
  assert isinstance(result, ResultProxy)
  rows = session.query(func.count(PureEligibleEmployeeJob.emplid)).scalar()
  assert rows > 0
