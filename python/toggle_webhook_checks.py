#!/usr/bin/env python3
import os
import time

import requests

WEBHOOKS = [
    # NOTE! Set the correct check names & webhook URLs here
    ('Check One', 'https://uptime.com/metrics/webhook/XXXXXXXXXXXX'),
    ('Check Two', 'https://uptime.com/metrics/webhook/XXXXXXXXXXXX'),
]


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def prompt_for_check():
    for i, check in enumerate(WEBHOOKS, start=1):
        print('{}: {}'.format(i, check[0]))

    try:
        selection = int(input('\nSelect Webhook check --> ')) - 1
        return WEBHOOKS[selection]
    except Exception:
        return None


def prompt_for_state():
    selection = input('\nSet check to [U]p, [D]own --> ').upper()
    if not selection or selection[0] not in ('U', 'D'):
        return None
    elif selection[0] == 'U':
        return True
    else:
        return False


def call_webhook_api(url, state):
    r = requests.post(url, json={'state_is_up': state})
    r.raise_for_status()


def main():
    while True:
        clear_screen()
        check = prompt_for_check()
        if not check:
            continue

        state = prompt_for_state()
        if state is None:
            continue

        print('\nCalling webhook API...')
        call_webhook_api(check[1], state)

        print('\nCheck "{}" was successfully set to state "{}".'.format(
            check[0], 'UP' if state else 'DOWN'))

        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
