import env
from pureapi import client, parser

r = client.get(
  'person',
  { 
    'window.size': 1,
    'namespaces': 'remove',
    'rendering': 'xml_long',
  }
)
for record in parser.records(r.text):
  person = parser.person(record)
  print(person)
  print("\n")

#for r in client.get_all('person'):
#  print(r.status_code)    
