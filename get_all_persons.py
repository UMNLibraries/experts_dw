import pure_api_client as client

params = { 
  'window.size': 20,
  'namespaces': 'remove',
  'rendering': 'xml_long',
}
count = 0
for response in client.get_all('person', params):
  with open('person_' + str(count) + '.xml', 'w') as file:
    print(response.text, file=file)
  count = count + 1
