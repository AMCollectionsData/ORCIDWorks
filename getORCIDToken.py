import requests
from decouple import config
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logfile_format = logging.Formatter('%(asctime)s: %(name)s (%(funcName)s): %(message)s')
logfile = logging.FileHandler(  filename='getORCIDtoken.log',
                                mode='a',
                                encoding=None,
                                delay=False )
logfile.setFormatter(logfile_format)
logfile.setLevel(logging.DEBUG)

log.addHandler(stream_handler)
log.addHandler(logfile)

testing = False

if testing:
    ORCID_API_ID = config('ORCID_SANDBOX_API_ID')
    ORCID_API_SECRET = config('ORCID_SANDBOX_API_SECRET')
else:
    ORCID_API_ID = config('ORCID_API_ID')
    ORCID_API_SECRET = config('ORCID_API_SECRET')

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
        service = 'sandbox.'
        log.info('In testing mode (using sandbox)')
    else:
        service = ''
        log.info('In production mode')

    tokenURL = 'https://' + service + 'orcid.org/oauth/token'

    try:
        response = requests.post(   url=tokenURL,
                                    headers=headers,
                                    data=auth )
        response.raise_for_status()
        if response.status_code == 200:
            ORCID_ACCESS_TOKEN = response.json()['access_token']
            log.info('Retrieving token from {0}...'.format(tokenURL))
            log.debug('Response code {0}'.format(response.status_code))
            return ORCID_ACCESS_TOKEN
    except requests.RequestException as error:
        log.exception(error)
        raise

def writeToken(token, testing):
    with open(".env", "a") as file:
        if testing == True:
            file.write("\n# Sandbox token\n")
        token_env = ('PUBLIC_ACCESS_TOKEN = \"{0}\"'.format(token))
        file.write(token_env)
        log.info("Added token to .env file.")
        file.close

if __name__ == '__main__':
    token = fetchToken(ORCID_API_ID, ORCID_API_SECRET, testing)
    log.info("Fetched token.")
    writeToken(token, testing)
