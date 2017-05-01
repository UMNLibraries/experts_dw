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

# Right now, this handles only ContributionToJournalType records.
def publication(record):
  publication = {  
    'pure_uuid': record.attrib['uuid'],
    # Hard-coded for now:
    'type': 'article-journal',
    'title': record.find('./title').text,
    'container_title': record.find('./journal/title/string').text,
    'persons': [],
  }

  scopus_id_elem = record.find("./external/secondarySource[@source='Scopus']")
  publication['scopus_id'] = scopus_id_elem.attrib['source_id'] if scopus_id_elem is not None else None

  pmid_elem = record.find("./external/secondarySource[@source='PubMed']")
  publication['pmid'] = pmid_elem.attrib['source_id'] if pmid_elem is not None else None

  # Seems there may be more than one of these in the Pure record, but we just use the 
  # first one for now.
  doi_elem = record.find('./dois/doi/doi')
  publication['doi'] = doi_elem.text if doi_elem is not None else None

  issn_elem = record.find('./journal/issn/string')
  publication['issn'] = issn_elem.text if issn_elem is not None else None

  volume_elem = record.find('./volume')
  publication['volume'] = volume_elem.text if volume_elem is not None else None

  issue_elem = record.find('./journalNumber')
  publication['issue'] = issue_elem.text if issue_elem is not None else None

  pages_elem = record.find('./pages')
  publication['pages'] = pages_elem.text if pages_elem is not None else None

  # TODO: So far, lots of records are missing this data. Is it missing from all of them?
  citation_total_elem = record.find('./citations/citationTotal')
  publication['citation_total'] = int(citation_total_elem.text) if citation_total_elem is not None else None

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
  print(publication)

  person_ordinal = 0
  for pure_person in record.findall('./persons/personAssociation'):
    person = {
      'first_name': pure_person.find('./name/firstName').text,
      'last_name': pure_person.find('./name/lastName').text,
      'ordinal': person_ordinal,
      'person_role': pure_person.find('./personRole/term/localizedString').text.lower(),
    }

    internal_person_elem = pure_person.find('./person')
    external_person_elem = pure_person.find('./externalPerson')
    if internal_person_elem is not None:
      person['emplid'] = internal_person_elem.find('./employeeId').text
      person_elem = internal_person_elem
    else:
      person['emplid'] = None
      person_elem = external_person_elem

    person['pure_uuid'] = person_elem.attrib['uuid']

    hindex_elem = person_elem.find('./hIndex')
    person['hindex'] = hindex_elem.attrib['hIndexTotal'] if hindex_elem is not None else None

    scopus_id_elem = person_elem.find("./external/secondarySource[@source='Scopus']")
    person['scopus_id'] = scopus_id_elem.attrib['source_id'] if scopus_id_elem is not None else None

    print('  ' + str(person))
    publication['persons'].append(person)
    person_ordinal = person_ordinal + 1

  return publication
