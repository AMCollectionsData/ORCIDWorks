# Python3.6
# Use an access token from the Hub to retrieve (all) users
# With the list of users, use the ORCID API proxy to retrieve their work summaries
# Done handle 403 responses by using a public read directly from ORCID
# Done change from json out to tsv
# Done make UTF-8 safe, much easier than I thought but seems to slow operation
# Done use time.sleep to control request/min and prevent overloading ORCID (max 8/sec to be safe)

from os import urandom
import requests
import time
from decouple import config

hubID = config('HUB_ID')
hubSecret = config('HUB_SECRET')

orcid_token = config('PUBLIC_ACCESS_TOKEN')

ORCID_API_version = "v3.0"

testing = True

def fetch_hub_access_token(id, secret, test):
    print("ID: {0}\nSecret: {1}\nTest: {2}\n".format(id, secret, test))
    auth = {
        'client_id': id,
        'client_secret': secret,
        'grant_type': 'client_credentials'
        }
    
    if test == True:
        service = "test."
    else:
        service = ''
    
    tokenURL = ('https://' + service + 'orcidhub.org.nz/oauth/token')

    response = requests.post(
        url = tokenURL,
        data = auth
    )
    if response.status_code == 200:
        hub_access_token = response.json()['access_token']
        print("Hub token: {0}.\n\n".format(hub_access_token))
        return hub_access_token
    else:
        raise Exception('Error: {0} {1}'.format(response.status_code, response.reason))

access_token = fetch_hub_access_token(hubID, hubSecret, testing)

if testing == True:
    hub_url = 'https://test.orcidhub.org.nz/api/v1/'
    member_orcid_url = 'https://test.orcidhub.org.nz/orcid/api/' + ORCID_API_version + '/'
    member_headers = {'accept': 'application/json', 'authorization': 'Bearer ' + access_token,
                      'accept-encoding': 'identity'}
    pub_orcid_url = 'https://pub.sandbox.orcid.org/' + ORCID_API_version + '/'
else:
    hub_url = 'https://orcidhub.org.nz/api/v1/'
    member_orcid_url = 'https://api.orcid.org/' + ORCID_API_version + '/'
    member_headers = {'accept': 'application/json', 'authorization': 'Bearer ' + access_token,
                      'accept-encoding': 'identity'}
    pub_orcid_url = 'https://pub.orcid.org/' + ORCID_API_version + '/'


public_headers = {
    'accept': 'application/json',
    'authorization': 'Bearer ' + orcid_access_token,
    'accept-encoding': 'identity'
    }

 
# def fetch_hub_users(token):
#     headers = {'accept': 'application/json', 'authorization': 'Bearer ' + token}
#     body = []
#     users_on_page = 1
#     page = 1
#     while users_on_page > 0:
#         response = requests.get(hub_url + 'users', headers=headers, params={'page': page})
#         if response.status_code == 200:
#             users_on_page = int(response.headers['pagination-count'])
#             for users in range(0, users_on_page-1):
#                 body.append(response.json()[users])
#             page += 1
#         elif response.status_code == 401:
#             raise Exception('Access token expired/revoked get a new one')
#         else:
#             raise Exception('Error: {0} {1}'.format(response.status_code, response.reason))
#     return body


# def fetch_works_list(token, orcid):
#     headers = {'accept': 'application/json', 'authorization': 'Bearer ' + token, 'accept-encoding': 'identity'}
#     response = requests.get(member_orcid_url + orcid + '/works', headers=headers)
#     status = response.status_code
#     if status == 401:
#         time.sleep(0.125)
#         response = requests.get(pub_orcid_url + orcid + '/works', headers=public_headers)
#     return response, status


# def fetch_work(token, orcid, putcode, status):
#     headers = {'accept': 'application/json', 'authorization': 'Bearer ' + token, 'accept-encoding': 'identity'}
#     response = requests.get(member_orcid_url + orcid + '/work/' +
#                             str(putcode), headers=headers)
#     if status == 401:
#         time.sleep(0.125)
#         response = requests.get(pub_orcid_url + orcid + '/work/' +
#                                 str(putcode), headers=public_headers)
#     return response


# def fetch_orcid_works(token):
#     pub_summaries = []
#     hub_users = fetch_hub_users(token)
#     if isinstance(hub_users, list):
#         for users in hub_users:
#             if users['confirmed'] and users['orcid']:
#                 response, status = fetch_works_list(token, users['orcid'])
#                 print(users['orcid'])
#                 pubs = response.json()['group']
#                 if pubs:
#                     for pub in pubs:
#                         pub_sum = pub['work-summary'][0]
#                         putcode = pub_sum['put-code']
#                         source = pub_sum['source']['source-name']
#                         external_id_type = ""
#                         external_id_value = ""
#                         if source:
#                             source = source['value']
#                         try:
#                             title = pub_sum['title']['title']['value']
#                         except (IndexError, TypeError):
#                             title = "No Title"
#                         try:
#                             if len(pub_sum['external-ids']['external-id'][0]['external-id-value']) > 0:
#                                 external_id_value = pub_sum['external-ids']['external-id'][0]['external-id-value']
#                                 external_id_type = pub_sum['external-ids']['external-id'][0]['external-id-type']
#                         except (IndexError, TypeError):
#                             external_id_value = ""
#                             external_id_type = ""
#                         pub_type = pub_sum['type']
#                         try:
#                             pub_year = pub_sum['publication-date']['year']['value']
#                         except (IndexError, TypeError):
#                             pub_year = ""
#                         visibility = pub_sum['visibility']
#                         pub_summaries.append({'email': users['email'], 'orcid': users['orcid'], 'status': status,
#                                               'put-code': putcode, 'source': source, 'title': title,
#                                               'external-id-type': external_id_type,
#                                               'external-id-value': external_id_value, 'type': pub_type,
#                                               'publication-date-year': pub_year, 'visibility': visibility,
#                                               'note': 'OK'})
#                 else:
#                     pub_summaries.append({'email': users['email'], 'orcid': users['orcid'], 'status': status,
#                                           'put-code': '', 'source': '', 'title': '', 'external-id-type': '',
#                                           'external-id-value': '', 'type': '', 'publication-date-year': '',
#                                           'visibility': '', 'note': 'No visible works'})
#             else:
#                 pub_summaries.append({'email': users['email'], 'orcid': users['orcid'], 'status': '',
#                                       'put-code': '', 'source': '', 'title': '', 'external-id-type': '',
#                                       'external-id-value': '', 'type': '', 'publication-date-year': '',
#                                       'visibility': '', 'note': 'ORCID iD not confirmed by Hub'})
#     return pub_summaries


# def fetch_work_details(token):
#     pub_details = []
#     pub_summaries = fetch_orcid_works(token)
#     for record in pub_summaries:
#         email = record['email']
#         orcid = record['orcid']
#         status = record['status']
#         putcode = record['put-code']
#         visibility = record['visibility']
#         source = record['source']
#         title = record['title']
#         external_id_type = record['external-id-type']
#         external_id_value = record['external-id-value']
#         external_id_url = None
#         external_id_relationship = None
#         pub_type = record['type']
#         pub_year = record['publication-date-year']
#         short_description = None
#         journal_title = None
#         citation_type = None
#         citation_value = None
#         url = None
#         language_code = None
#         country = None
#         note = record['note']
#         if record['put-code']:
#             response = fetch_work(token, record['orcid'], record['put-code'], record['status'])
#             work = response.json()
#             short_description = work['short-description']
#             try:
#                 journal_title = work['journal-title']['value']
#             except (IndexError, TypeError):
#                 pass
#             try:
#                 if len(work['citation']) > 0:
#                     citation_type = work['citation']['citation-type']
#                     citation_value = work['citation']['citation-value']
#                     citation_value = citation_value.strip()
#             except (IndexError, TypeError):
#                 pass
#             try:
#                 external_id_url = work['external-ids']['external-id'][0]['external-id-url']['value']
#             except (IndexError, TypeError):
#                 pass
#             if external_id_value:
#                 external_id_relationship = work['external-ids']['external-id'][0]['external-id-relationship']
#             try:
#                 url = work['url']['value']
#             except (IndexError, TypeError):
#                 pass
#             language_code = work['language-code']
#             try:
#                 country = work['country']['value']
#             except (IndexError, TypeError):
#                 pass
#         pub_details.append({'email': email, 'orcid': orcid, 'status': status, 'put-code': putcode,
#                             'visibility': visibility, 'source': source, 'title': title, 'journal-title': journal_title,
#                             'short-description': short_description, 'citation-type': citation_type,
#                             'citation-value': citation_value, 'external-id-type': external_id_type,
#                             'external-id-value': external_id_value, 'external-id-url': external_id_url,
#                             'external-id-relationship': external_id_relationship, 'type': pub_type,
#                             'publication-date-year': pub_year, 'url': url, 'language-code': language_code,
#                             'country': country, 'note': note})
#     return pub_details


# def write_works(token):
#     i = 0
#     outfile = open('organisation_works.tsv', 'w', encoding='utf-8')
#     row_headings = 'Email\tORCID iD\tResponse\tPut-Code\tVisibility\tSource\tTitle\tJournal Title\tShort Description' \
#                    '\tCitation Type\tCitation Value\tExternal ID Type\tExternal ID Value\tExternal ID URL' \
#                    '\tExternal ID Relationship\tType\tPublication Year\tURL\tLanguage Code\tCountry\tNote\n'
#     outfile.write(row_headings)
#     pub_summaries = fetch_work_details(token)
#     for record in pub_summaries:
#         row_data = '\t'.join(str(record[value]) for value in record) + '\n'
#         outfile.write(row_data)
#         i += 1
#     outfile.close()
#     return str(i) + ' rows written to file'


# print(write_works(access_token))