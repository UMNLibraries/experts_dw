from setuptools import setup, find_packages

setup(
  name='experts_dw',
  version='0.0.0',
  description='Tools for working with the Experts@Minnesota Data Warehouse.',
  url='https://github.com/UMNLibraries/experts_dw',
  author='David Naughton',
  author_email='nihiliad@gmail.com',
  packages=find_packages(exclude=['alembic','tests','docs','legacy','sql_acme','sql-developer-reports'])
)
