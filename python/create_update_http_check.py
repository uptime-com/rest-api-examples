#!/usr/bin/env python3
import argparse

import requests


def parse_args():
    parser = argparse.ArgumentParser(description='Create and modify a sample HTTP check.')
    parser.add_argument('--token', required=True,
                        help='Your Uptime.com API Token')
    parser.add_argument('--api', default='https://uptime.com/api/v1/',
                        help='(optional) The Uptime.com API endpoint to use, eg. '
                             'https://uptime.com/api/v1/')

    return parser.parse_args()


opts = parse_args()
headers = {'Authorization': 'token ' + opts.token}

print('\n1. Creating HTTP check...')
r = requests.post(opts.api + 'checks/add-http/',
                  headers=headers,
                  json={
                      'name': 'API Sample: HTTP Create & Update',
                      'msp_interval': 5,
                      'msp_address': 'http://google.com',
                      'contact_groups': ['Default'],
                      'locations': ['US-East', 'US-West', 'GBR'],
                  })
print(r.text)
r.raise_for_status()
check_pk = r.json()['results']['pk']

print('\n2. Updating interval...')
r = requests.patch(opts.api + 'checks/{pk}/'.format(pk=check_pk),
                  headers=headers,
                  json={
                      'msp_interval': 3,
                  })
print(r.text)
r.raise_for_status()


print('\n3. Updating contacts...')
r = requests.patch(opts.api + 'checks/{pk}/replace-contact-groups/'.format(pk=check_pk),
                  headers=headers,
                  json={
                      'contact_groups': ['Default'],
                  })
print(r.text)
r.raise_for_status()


print('\n4. Updating locations...')
r = requests.patch(opts.api + 'checks/{pk}/replace-locations/'.format(pk=check_pk),
                  headers=headers,
                  json={
                      'locations': ['US-East', 'GBR'],
                  })
print(r.text)
r.raise_for_status()


print('\n5. Creating tag...')
r = requests.post(opts.api + 'check-tags/',
                  headers=headers,
                  json={
                      'tag': 'API Sample Tag',
                      'color_hex': '#51e898',
                  })
print(r.text)


print('\n6. Assigning tag to check...')
r = requests.patch(opts.api + 'checks/{pk}/replace-tags/'.format(pk=check_pk),
                  headers=headers,
                  json={
                      'tags': ['API Sample Tag'],
                  })
print(r.text)
r.raise_for_status()


print('\n7. Pause check...')
r = requests.post(opts.api + 'checks/{pk}/pause/'.format(pk=check_pk),
                  headers=headers)
print(r.text)
r.raise_for_status()


print('\n8. Resume check...')
r = requests.post(opts.api + 'checks/{pk}/resume/'.format(pk=check_pk),
                  headers=headers)
print(r.text)
r.raise_for_status()
