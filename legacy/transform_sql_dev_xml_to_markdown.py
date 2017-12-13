# Transform SQL-Developer-generated XML report to Markdown. 

import sql_developer_report_parser as parser
import sys
filename = sys.argv[1]

for table in parser.tables(filename):
  print('### ' + table['name'])
  print("\n" + table['description'] + "\n")

  print('| Column | Description |')
  print('| ------ | ----------- |')
  for column in table['columns']:
    print('| ' + column['name'] + ' | ' + column['description'] + ' |')
