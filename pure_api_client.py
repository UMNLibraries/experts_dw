from dotenv import load_dotenv, find_dotenv
import os
import requests

load_dotenv(find_dotenv())

pure_api_url = os.environ.get('PURE_API_URL')
pure_api_user = os.environ.get('PURE_API_USER')
pure_api_pass = os.environ.get('PURE_API_PASS')

def get(family, window_size):
  return requests.get(
    pure_api_url + family,
    auth=(pure_api_user, pure_api_pass),
    params={'window.size': window_size, 'namespaces': 'remove'}
  )
