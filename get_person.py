import pure_api_client as client
import pure_api_response_parser as parser

r = client.get(
  'person',
  { 
    'window.size': 20,
    'namespaces': 'remove',
    'rendering': 'xml_long',
  }
)
for record in parser.records(r.text):
  person = parser.person(record)
  print(person)
  print("\n")

#for r in pure_api_client.get_all('person'):
#  print(r.status_code)    
