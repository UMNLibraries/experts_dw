import xml.etree.ElementTree as et

def records(xml):
  root = et.fromstring(xml)
  return root.findall('result/content')

def person(record):
  person = {  
    'pure_uuid': record.attrib['uuid'],
    'first_name': record.find('./name/firstName').text,
    'last_name': record.find('./name/lastName').text,
    'emplid': record.find('./employeeId').text,
  }

  hindex_elem = record.find('./hIndex')
  person['hindex'] = hindex_elem.attrib['hIndexTotal'] if hindex_elem is not None else None

  scopus_id_elem = record.find("./external/secondarySource[@source='Scopus']")
  person['scopus_id'] = scopus_id_elem.attrib['source_id'] if scopus_id_elem is not None else None

  return person

def publication(record):
  publication = {  
    'pure_uuid': record.attrib['uuid'],
    'title': record.find('./title').text,
  }

  year = record.find('./publicationDate/year').text
  issued_precision = 366
  month = '01'
  day = '01'
  month_elem = record.find('./publicationDate/month')
  if (month_elem is not None):
    month = month_elem.text
    if len(month) == 1:
      month = '0' + month
    issued_precision = 31
  day_elem = record.find('./publicationDate/day')
  if (day_elem is not None):
    day = day_elem.text
    if len(day) == 1:
      day = '0' + day
    issued_precision = 1
  publication['issued'] = '-'.join([year, month, day])
  publication['issued_precision'] = issued_precision

  return publication
