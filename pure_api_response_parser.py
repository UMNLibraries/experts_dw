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
