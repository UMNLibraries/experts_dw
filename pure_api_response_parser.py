import xml.etree.ElementTree as et
import re

def records(xml):
  root = et.fromstring(xml)
  return root.findall('result/content')

def person(person_elem):
  person = {
    'pure_uuid': person_elem.attrib['uuid'],
    'first_name': person_elem.find('./name/firstName').text,
    'last_name': person_elem.find('./name/lastName').text,

    # We default to internal. Parent elements will have context to set it otherwise.
    'pure_internal': 'Y',

    # Defaults for UMN-external persons:
    'emplid': None,
    'internet_id': None,
    'hindex': None,
    'scopus_id': None,
  }

  emplid_elem = person_elem.find('./employeeId')
  person['emplid'] = emplid_elem.text if emplid_elem is not None else None

  for link_id_elem in person_elem.findall('./linkIdentifiers/linkIdentifier/linkIdentifier'):
    if re.match('umn:', link_id_elem.text):
      # Pure prefixes internet IDs with 'umn:', which we remove:
      person['internet_id'] = link_id_elem.text[4:]
      # Should be only one internet ID:
      break

  # TODO: Will we always have an hindex for internal persons?
  hindex_elem = person_elem.find('./hIndex')
  person['hindex'] = hindex_elem.attrib['hIndexTotal'] if hindex_elem is not None else None

  scopus_id_elem = person_elem.find("./external/secondarySource[@source='Scopus']")
  person['scopus_id'] = scopus_id_elem.attrib['source_id'] if scopus_id_elem is not None else None

  return person

def person_association(person_assoc_elem):
  person_assoc = {
    'first_name': person_assoc_elem.find('./name/firstName').text,
    'last_name': person_assoc_elem.find('./name/lastName').text,
    'person_role': person_assoc_elem.find('./personRole/term/localizedString').text.lower(),
    # This will be set by the calling code (e.g. publication()):
    'ordinal': None,
  }
  internal_person_elem = person_assoc_elem.find('./person')
  external_person_elem = person_assoc_elem.find('./externalPerson')
  if internal_person_elem is not None:
    person_assoc['person'] = person(internal_person_elem)
  else:
    person_assoc['person'] = person(external_person_elem)
    person_assoc['person']['pure_internal'] = 'N'
  
  return person_assoc

def organisation(record):
  org = {
    'pure_uuid': record.attrib['uuid'],
    'parent_pure_uuid': None,
    'parent_pure_id': None,
    'type': record.find("./typeClassification/term/localizedString[@locale='en_US']").text.lower(),
  }

  # Hard-coded for now. Will need to change once we start importing external orgs.
  org['pure_internal'] = 'Y'

  # These fields will exist only for internal orgs:
  pure_id_elem = record.find("./external/secondarySource[@source='synchronisedOrganisation']")
  org['pure_id'] = pure_id_elem.attrib['source_id'] if pure_id_elem is not None else None

  name_en_elem = record.find("./name/localizedString[@locale='en_US']")
  org['name_en'] = name_en_elem.text if name_en_elem is not None else None

  name_variant_elem = record.find("./nameVariant/classificationDefinedFieldExtension/value/localizedString[@locale='en_US']")
  org['name_variant_en'] = name_variant_elem.text if name_variant_elem is not None else None

  url_elem = record.find("./webAddresses/classificationDefinedFieldExtension/value/localizedString[@locale='en_US']")
  org['url'] = url_elem.text if url_elem is not None else None

  parent_org_elem = record.find('./organisations/organisation')
  if parent_org_elem is not None:
    org['parent_pure_uuid'] = parent_org_elem.attrib['uuid']
    parent_pure_id_elem = parent_org_elem.find("./external/secondarySource[@source='synchronisedOrganisation']")
    org['parent_pure_id'] = parent_pure_id_elem.attrib['source_id'] if parent_pure_id_elem is not None else None


  return org

# Right now, this handles only ContributionToJournalType records.
def publication(record):
  publication = {  
    'pure_uuid': record.attrib['uuid'],
    # Hard-coded for now:
    'type': 'article-journal',
    'title': record.find('./title').text,
    'container_title': record.find('./journal/title/string').text,
    'person_associations': [],
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
  for person_assoc_elem in record.findall('./persons/personAssociation'):
    person_assoc = person_association(person_assoc_elem)
    person_assoc['ordinal'] = person_ordinal
    print('  ' + str(person_assoc))
    publication['person_associations'].append(person_assoc)
    person_ordinal = person_ordinal + 1

  return publication
