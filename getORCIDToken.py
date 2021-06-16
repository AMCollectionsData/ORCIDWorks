import requests
import time
from decouple import config

ORCID_API_ID = config('ORCID_API_ID')
ORCID_API_SECRET = config('ORCID_API_SECRET')

testing = False

def fetchToken(id, secret, sandbox):
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
        print ("NB: Running in testing mode (using sandbox).")
    else:
        service = ''

    tokenURL = 'https://' + service + 'orcid.org/oauth/token'

    response = requests.post(
        url=tokenURL,
        headers=headers,
        data=auth
    )

    print('Retrieving token from {0}...'.format(tokenURL))

    if response.status_code == 200:
        ORCID_ACCESS_TOKEN = response.json()['access_token']
        return ORCID_ACCESS_TOKEN
    else:
        raise Exception('Error: {0} {1}'.format(response.status_code, response.text))

token = fetchToken(ORCID_API_ID, ORCID_API_SECRET, testing)

with open(".env", "a") as file:
    newline = ("PUBLIC_ACCESS_TOKEN = \"{0}\"".format(token))
    file.write(newline)
    print ("Added token '{0}' to .env file.".format(token))
    file.close