from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from experts_dw import dbviews
from sqlalchemy.engine import ResultProxy

def test_pure_eligible_affiliates():
  result = dbviews.create_pure_eligible_affiliates()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_employees():
  result = dbviews.create_pure_eligible_employees()
  assert isinstance(result, ResultProxy)

def test_pure_eligible_persons():
  result = dbviews.create_pure_eligible_persons()
  assert isinstance(result, ResultProxy)

def test_employee_jobs_current():
  result = dbviews.create_employee_jobs_current()
  assert isinstance(result, ResultProxy)
