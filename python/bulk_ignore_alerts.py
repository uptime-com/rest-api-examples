#!/usr/bin/env python3
import argparse
import datetime as dt
import time

import requests


def date(d):
    return dt.datetime.strptime(d, '%Y-%m-%d').date()


def parse_args():
    parser = argparse.ArgumentParser(description='Ignore alerts between date ranges for '
                                                 'one or more checks.')
    parser.add_argument('--token', required=True,
                        help='Your Uptime.com API Token')
    parser.add_argument('--api', default='https://uptime.com/api/v1/',
                        help='(optional) The Uptime.com API endpoint to use, eg. '
                             'https://uptime.com/api/v1/')
    parser.add_argument('--from', required=True, type=date,
                        help='The earliest date to ignore alerts from, in YYYY-MM-DD format.')
    parser.add_argument('--to', required=True, type=date,
                        help='The latest date to ignore alerts from, in YYYY-MM-DD format.')
    parser.add_argument('--prefix', required=True,
                        help='The check name or check name prefix to ignore alerts for.')
    parser.add_argument('--subaccount', type=int,
                        help='(optional) A subaccount to process instead of the main account.')

    return parser.parse_args()


opts = parse_args()
headers = {'Authorization': 'token ' + opts.token}
if opts.subaccount:
    headers['X-Subaccount'] = str(opts.subaccount)


def ignore_alert(outage):
    """
    Call the API to ignore the alert for this outage.
    """
    print('Ignoring: {} @ {}'.format(outage['check_name'], outage['created_at']))
    r = requests.post(outage['ignore_alert_url'], headers=headers)
    r.raise_for_status()

    # Delay to keep within rate limits
    time.sleep(2.2)


page = 0
while True:
    # Read through each page of outages between the given dates
    page += 1
    r = requests.get(opts.api + 'outages/',
                    headers=headers,
                    params={
                        'start_date': str(getattr(opts, 'from')),
                        'end_date': str(opts.to),
                        'page_size': 250,
                        'page': page,
                    })

    r.raise_for_status()
    outages = r.json()['results']
    if not outages:
        break

    # For each outage matching the check name prefix, ignore the outage
    for outage in outages:
        if outage['check_name'].startswith(opts.prefix) and not outage['ignored']:
            ignore_alert(outage)
