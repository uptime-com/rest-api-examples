#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import sys
from urllib.parse import urlencode

import requests

CONFIG = {
    'api': 'https://uptime.com/api/v1/',
    'token': '',
    'headers': {},
    'page_size': 250,
}


def parse_date(d):
    return dt.datetime.strptime(d, '%Y-%m-%d').date()


def parse_args():
    parser = argparse.ArgumentParser(description='Download stats in bulk for all checks.')
    parser.add_argument('--token', required=True,
                        help='Your Uptime.com API Token')
    parser.add_argument('--api',
                        help='(optional) The Uptime.com API endpoint to use, eg. '
                             'https://uptime.com/api/v1/')
    parser.add_argument('-d', '--date', required=True, type=parse_date,
                        help='Date to start saving statistics from, YYYY-MM-DD')

    return parser.parse_args()


def make_api_call(label, method, endpoint, pk=None, params=None, json=None):
    """Make an Uptime.com API call with the given method, endpoint and parameters."""
    url = CONFIG['api'] + endpoint.format(pk=pk)
    qs = '?' + urlencode(params) if params else ''
    sys.stderr.write('{} - {} {}{}\n'.format(label, method.upper(), url, qs))

    r = requests.request(method, url, params=params, json=json, headers=CONFIG['headers'])
    r.raise_for_status()
    return r.json()


def load_all_checks_stats(from_date):
    """Load info and stats for all checks in the account, spanning multiple pages
    of results if necessary."""
    page = 1
    stats = {}
    while True:
        r = make_api_call('Loading checks (page {})'.format(page),
                          'get', 'checks/',
                          params={'page': page, 'page_size': CONFIG['page_size']})
        next_page = r['next']
        pks = [chk['pk'] for chk in r['results']]
        stats.update({chk['pk']: chk for chk in r['results']})

        r = make_api_call('Reading check stats (page {})'.format(page),
                          'get', 'checks/bulk/stats/',
                          params={'pk': ','.join(str(pk) for pk in pks),
                                  'start_date': str(from_date),
                                  'include_alerts': '1'})
        for stat in r['checks']:
            stats[stat['pk']].update(stat)

        if not next_page:
            break
        else:
            page += 1

    return sorted(stats.values(), key=lambda x: x['pk'])


def main():
    """Program entry point."""
    opts = parse_args()
    CONFIG['api'] = opts.api or CONFIG['api']
    CONFIG['headers'] = {'Authorization': 'token ' + opts.token}

    stats = load_all_checks_stats(opts.date)
    print(json.dumps(stats, indent=4))


if __name__ == '__main__':
    main()
