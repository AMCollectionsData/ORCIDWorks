import requests
import time
from decouple import config

ORCID_API_ID = config('ORCID_API_ID')
ORCID_API_SECRET = config('ORCID_API_SECRET')

testing = True

def fetch_orcid_access_token(id, secret, sandbox):
    print("ID: {0}\nSecret: {1}\nSandbox: {2}\n".format(id, secret, sandbox))
    auth = {
        'client_id': id,
        'client_secret': secret,
        'grant_type': 'client_credentials',
        'scope': '/read-public'
        }
    headers = {
        'accept': 'application/json'
    }
    
    if sandbox == True:
        service = "sandbox."   
    else:
        service = ''

    tokenURL = 'https://' + service + 'orcid.org/oauth/token/'
    print('URL: {0}\n'.format(tokenURL))

    response = requests.post(
        url=tokenURL,
        headers=headers,
        data=auth
    )

    print(response.type())


    # if response.status_code == 200:
    #     hub_access_token = response.json()['access_token']
    #     print("ORCID token: {0}\n\n".format(hub_access_token))
    #     return hub_access_token
    # else:
    #     raise Exception('Error: {0} {1}'.format(response.status_code, response.text))

fetch_orcid_access_token(ORCID_API_ID, ORCID_API_SECRET, testing)