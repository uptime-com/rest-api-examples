#!/usr/bin/env python3
import argparse
import datetime as dt
import time
from urllib.parse import urlencode

import requests

CONFIG = {
    'api': 'https://uptime.com/api/v1/',
    'token': '',
    'headers': {},
    'page_size': 250,
}


def parse_args():
    parser = argparse.ArgumentParser(description='Monitor checks & alerts in real-time '
                                                 'without exceeding API fair use limits.')
    parser.add_argument('--token', required=True,
                        help='Your Uptime.com API Token')
    parser.add_argument('--api',
                        help='(optional) The Uptime.com API endpoint to use, eg. '
                             'https://uptime.com/api/v1/')

    return parser.parse_args()


def make_api_call(label, method, endpoint, pk=None, params=None, json=None):
    """Make an Uptime.com API call with the given method, endpoint and parameters."""
    url = CONFIG['api'] + endpoint.format(pk=pk)
    qs = '?' + urlencode(params) if params else ''
    print('{} - {} {}{}'.format(label, method.upper(), url, qs))

    r = requests.request(method, url, params=params, json=json, headers=CONFIG['headers'])
    r.raise_for_status()
    return r.json()


def load_all_checks():
    """Load all checks in the account, spanning multiple pages of results if necessary."""
    page = 1
    all_checks = []
    while True:
        r = make_api_call('Loading checks (page {})'.format(page),
                          'get', 'checks/',
                          params={'page': page, 'page_size': CONFIG['page_size']})
        all_checks.extend(r['results'])
        if not r['next']:
            break
        else:
            page += 1

    return {c['pk']: {
        'pk': c['pk'],
        'name': c['name'],
        'is_paused': c['is_paused'],
        'state_is_up': c['state_is_up'],
        'state_changed_at': c['state_changed_at'],
    } for c in all_checks}


def load_alerts_from_date(from_date):
    """Load all new alerts raised after the given date, spanning multiple pages if necessary."""
    page = 1
    all_alerts = []
    while True:
        r = make_api_call('Loading alerts since {} (page {})'.format(from_date, page),
                          'get', 'alerts/',
                          params={'ordering': '-pk', 'start_date': from_date.isoformat(),
                                  'page_size': CONFIG['page_size']})
        all_alerts.extend(r['results'])
        if len(r['results']) < CONFIG['page_size']:
            break
        else:
            page += 1

    # Reverse the list so earlier alerts come first, to be overwritten by later ones.
    return list(reversed([{
        'check_pk': a['check_pk'],
        'state_is_up': a['state_is_up'],
        'state_changed_at': a['created_at'],
    } for a in all_alerts]))


def merge_alerts_into_check_status(all_checks, new_alerts):
    for alert in new_alerts:
        check = all_checks[alert['check_pk']]
        check['state_is_up'] = alert['state_is_up']
        check['state_changed_at'] = alert['state_changed_at']

        print('NEW ALERT: {} - {} at {}'.format(
            check['name'],
            'UP' if check['state_is_up'] else 'DOWN',
            check['state_changed_at']))


def display_check_status(checks):
    """Print out the status of all down checks."""
    down = sorted((c for c in checks.values() if not c['state_is_up']),
                  key=lambda x: x['name'])

    print('')
    print('------------')
    print('CHECK STATUS')
    print('------------')
    print('{} total checks.'.format(len(checks)))

    if not down:
        print('No checks are currently down.\n')
        return

    for check in down:
        print('{:40s} - DOWN since {}'.format(check['name'], check['state_changed_at']))
    print('')


def main():
    """Program entry point."""
    opts = parse_args()
    CONFIG['api'] = opts.api or CONFIG['api']
    CONFIG['headers'] = {'Authorization': 'token ' + opts.token}

    all_checks = []
    minutes_elapsed = 0
    last_load = dt.datetime.utcnow()
    while True:
        from_date = last_load
        last_load = dt.datetime.utcnow()

        if minutes_elapsed % 15 == 0:
            # Reload the status of all checks every 15 minutes, loading new checks etc.
            all_checks = load_all_checks()
        else:
            # Otherwise check for new alerts and update the checks statuses.
            new_alerts = load_alerts_from_date(from_date)
            merge_alerts_into_check_status(all_checks, new_alerts)

        # Show a printout of current status
        display_check_status(all_checks)

        # Wait for 1 minute which is the minimum interval at which new alerts can be received
        print('Waiting 1 minute, Ctrl+C to exit...')
        time.sleep(60)
        minutes_elapsed += 1


if __name__ == '__main__':
    main()
