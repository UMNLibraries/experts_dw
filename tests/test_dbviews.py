from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from experts_dw import dbviews
from sqlalchemy.engine import ResultProxy

def test_employee_jobs_current():
  result = dbviews.create_employee_jobs_current()
  assert isinstance(result, ResultProxy)
