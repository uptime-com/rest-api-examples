#!/usr/bin/env python3
import argparse

import requests


def parse_args():
    parser = argparse.ArgumentParser(description='Delete all API sample checks named '
                                                 '"API Sample: ..."')
    parser.add_argument('--token', required=True,
                        help='Your Uptime.com API Token')
    parser.add_argument('--api', default='https://uptime.com/api/v1/',
                        help='(optional) The Uptime.com API endpoint to use, eg. '
                             'https://uptime.com/api/v1/')

    return parser.parse_args()


opts = parse_args()
headers = {'Authorization': 'token ' + opts.token}

print('\n1. Search for checks that include "API Sample:"...')
r = requests.get(opts.api + 'checks/',
                 headers=headers,
                 params={
                    'search': "API Sample:",
                    'page_size': 250
                 })
print(r.text)
r.raise_for_status()
checks = r.json()['results']


print('\n2. Delete each check whose name starts with "API Sample:"...')
for check in checks:
    if check['name'].startswith('API Sample:'):
        print('DELETE - ' + check['name'])
        r = requests.delete(opts.api + 'checks/{pk}/'.format(pk=check['pk']),
                            headers=headers)
        print(r.text)
        print('')
        r.raise_for_status()
