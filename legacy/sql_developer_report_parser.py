import xml.etree.ElementTree as et

def tables(filename):
  ns = {'t': 'http://oracle.com/datamodeler/reports/tables'}
  root = et.parse(filename).getroot()
  tables = []
  for table_details in root.findall('t:TablesCollection/t:TableDetails', ns):
    table = {
      'name': table_details.find('t:TableName', ns).text[7:],
      'description': table_details.find('t:DescriptionNotes/t:Description/t:DescriptionDetails/t:DescriptionRow', ns).text,
      'columns': [],
    }
    for column_details in table_details.findall('t:ColumnsCommentsCollection/t:ColumnCommentsDetails', ns):
      table['columns'].append({
        'name': column_details.find('t:ColumnCommentsName', ns).text,
        'description': column_details.find('t:ColumnDescription/t:ColumnDescriptionDetails/t:ColumnDescriptionRow', ns).text,
      })
    tables.append(table)
  return tables
