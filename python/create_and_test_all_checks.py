#!/usr/bin/env python3
import argparse
import time
import json
import random
import requests

API_URL = ''
TOKEN = ''
CONTACT_GROUPS = []
LOCATIONS = ['US-East', 'US-West']
TAGS = []


def call_api(method, data=None):
    headers = {
        'Authorization': 'Token %s' % TOKEN
    }
    url = API_URL + method
    if data is None:
        res = requests.get(url, headers=headers)
    else:
        res = requests.post(url, json=data, headers=headers)
    res = res.json()
    if 'messages' in res:
        if res['messages']['errors']:
            msg = res['messages']
            text = '%s: %s' % (msg['error_code'], msg['error_message'])
            if 'error_fields' in msg:
                text += ' Field errors: '
                for k, v in msg['error_fields'].items():
                    text += '%s: %s' % (k, v)
            raise Exception(text)
        return res['results']
    return res


def gen_name(initial):
    return '%s_%s' % (initial, ''.join(random.choices('01234567890abcdef', k=5)))


def create_api_check(url, status_code):
    script = [{
        "step_def":"C_GET",
        "values": {
            "url": url,
            "headers":{}
            }
    }, {
        "step_def":"V_HTTP_STATUS_CODE_IS",
        "values":{
            "status_code": status_code,
        }
    }]

    params = {
        "name": gen_name("API_TEST_API"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 5,
        "msp_sensitivity": 1,
        "msp_num_retries": 1,
        "msp_use_ip_version": "IPV4",
        "msp_address": "httpbin.org",
        "msp_threshold": 0,
        "msp_script": json.dumps(script),
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-api/', data=params)


def create_http_check(url):
    params = {
        "name": gen_name("API_TEST_HTTP"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "",
        "msp_address": url,  # full URL of the page to check
        #"msp_port": "443",
        "msp_username": "",
        "msp_password": "",
        "msp_send_string": "",
        "msp_expect_string": "",
        "msp_expect_string_type": "STRING",  # STRING, REGEX or INVERSE_REGEX
        "msp_threshold": 10,  # threshold for the response time or page load time
        "msp_headers": "",
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-http/', data=params)


def create_blacklist_check(domain):
    params = {
        "name": gen_name("API_TEST_BLACKLIST"),
        "contact_groups": CONTACT_GROUPS,
        "locations": [],
        "tags": TAGS,
        "msp_num_retries": 2,
        "msp_address": domain,
        "msp_notes": ""
    }
    return call_api('/checks/add-blacklist/', data=params)


def create_dns_check(domain, dns_server, a_record):
    params = {
        "name": gen_name("API_TEST_DNS"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_address": domain,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_dns_server": "",
        "msp_dns_record_type": "A",  # ANY, A, AAAA, CNAME, MX, NS, PTR, SOA or TXT
        "msp_expect_string": a_record,
        "msp_threshold": 20,
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-dns/', data=params)


def create_icmp_check(address):
    params = {
        "name": gen_name("API_TEST_ICMP"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "IPV4",
        "msp_address": address,
        "msp_notes": "",
        "msp_include_in_global_metrics": True
      }
    return call_api('/checks/add-icmp/', data=params)


def create_imap_check(server, port, use_tls=True):
    params = {
        "name": gen_name("API_TEST_IMAP"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "IPV4",
        "msp_address": server,
        "msp_port": port,
        "msp_expect_string": "",
        "msp_encryption": "SSL_TLS" if use_tls else "",
        "msp_notes": "",
        "msp_include_in_global_metrics": True
      }
    return call_api('/checks/add-imap/', data=params)


def create_malware_check(domain):
    params = {
        "name": gen_name("API_TEST_MALWARE"),
        "contact_groups": CONTACT_GROUPS,
        "locations": [],
        "tags": TAGS,
        "msp_num_retries": 2,
        "msp_address": domain,
        "msp_notes": ""
    }
    return call_api('/checks/add-malware/', data=params)


def create_ntp_check(address, port=123):
    params = {
        "name": gen_name("API_TEST_NTP"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "IPV4",
        "msp_address": address,
        "msp_port": 123,
        "msp_threshold": 1,
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-ntp/', data=params)


def create_pop_check(server, port, use_tls=True):
    params = {
        "name": gen_name("API_TEST_POP"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "IPV4",
        "msp_address": server,
        "msp_port": port,
        "msp_expect_string": "",
        "msp_encryption": "SSL_TLS" if use_tls else True,
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-pop/', data=params)


def create_rum_check(domain):
    params = {
        "name": gen_name("API_TEST_RUM"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_address": domain,
        "msp_threshold": 30,
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-rum/', data=params)


def create_smtp_check(server, port, use_tls=True):
    params = {
        "name": gen_name("API_TEST_SMTP"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "IPV4",
        "msp_address": server,
        "msp_port": port,
        "msp_expect_string": "",
        "msp_encryption": "SSL_TLS" if use_tls else "",
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-smtp/', data=params)


def create_ssh_check(server, port=22):
    params = {
        "name": gen_name("API_TEST_SSH"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "IPV4",
        "msp_address": server,
        "msp_port": port,
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-ssh/', data=params)


def create_ssl_check(domain, port=443, protocol='http'):
    params = {
        "name": gen_name("API_TEST_SSL"),
        "contact_groups": CONTACT_GROUPS,
        "locations": [],
        "tags": TAGS,
        "msp_num_retries": 2,
        "msp_address": domain,
        "msp_port": port,
        "msp_protocol": protocol,  # "http", "smtp", "pop3", "imap", "ftp", "xmpp", "irc", and "ldap"
        "msp_threshold": 10,
        "msp_notes": ""
    }
    return call_api('/checks/add-ssl-cert/', data=params)


def create_tcp_check(server, port, send, expect):
    params = {
        "name": gen_name("API_TEST_TCP"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "",
        "msp_address": server,
        "msp_port": port,
        "msp_send_string": send,
        "msp_expect_string": expect,
        "msp_expect_string_type": "STRING",
        "msp_threshold": 10,
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-tcp/', data=params)


def create_transaction_check(open_url, expect_status):
    script = [{
        "step_def":"C_OPEN_URL",
        "values": {
            "url": open_url,
            "headers":{}
            }
    }, {
        "step_def":"V_HTTP_STATUS_CODE_IS",
        "values":{
            "http_status": expect_status
        }
    }]

    params = {
        "name": gen_name("API_TEST_TRANSACTION"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 5,
        "msp_sensitivity": 1,
        "msp_num_retries": 1,
        "msp_use_ip_version": "IPV4",
        "msp_address": "httpbin.org",
        "msp_threshold": 0,
        "msp_script": json.dumps(script),
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-transaction/', data=params)


def create_udp_check(address, port, send_string, expect_string):
    params = {
        "name": gen_name("API_TEST_UDP"),
        "contact_groups": CONTACT_GROUPS,
        "locations": LOCATIONS,
        "tags": TAGS,
        "msp_interval": 1,
        "msp_sensitivity": 2,
        "msp_num_retries": 2,
        "msp_use_ip_version": "",
        "msp_address": address,
        "msp_port": port,
        "msp_send_string": send_string,
        "msp_expect_string": expect_string,
        "msp_expect_string_type": "STRING",
        "msp_threshold": 10,
        "msp_notes": "",
        "msp_include_in_global_metrics": True
    }
    return call_api('/checks/add-udp/', data=params)


def create_whois_check(domain, days_to_expire=30, registrar=None, nameservers=None):
    expect_string = ''
    if registrar is not None:
        expect_string += 'registrar: %s' % registrar
    if nameservers is not None:
        expect_string += 'nameservers: %s' % ','.join(nameservers)
    params = {
        "name": gen_name("API_TEST_WHOIS"),
        "contact_groups": CONTACT_GROUPS,
        "locations": [],
        "tags": TAGS,
        "msp_num_retries": 2,
        "msp_address": domain,
        "msp_expect_string": expect_string,
        "msp_threshold": days_to_expire,
        "msp_notes": ""
    }
    return call_api('/checks/add-whois/', data=params)


def up_or_down(status):
    return 'UP' if status else 'DOWN'


def create_checks():
    parse_args()
    print("Creating checks...")
    defs = [
        # Function, Params, expected check state: UP - True | DOWN - False
        [create_api_check, ["https://uptime.com", "200"], True],
        [create_api_check, ["https://uptime.com", "404"], False],

        [create_http_check, ['http://uptime.com'], True],
        [create_http_check, ['http://fakeserver123.com'], False],

        [create_icmp_check, ['1.1.1.1'], True],
        [create_icmp_check, ['1.2.3.4'], False],

        [create_ntp_check, ['0.north-america.pool.ntp.org'], True],
        [create_ntp_check, ['ntp.fakeserver123.com'], False],

        [create_tcp_check, ['uptime.com', 80, '', ''], True],
        [create_tcp_check, ['fakeserver123.com', 80, 'test', 'test'], False],

        [create_transaction_check, ['http://uptime.com', "200"], True],
        [create_transaction_check, ['http://uptime.com', "404"], False],

        [create_pop_check, ['pop.yandex.com', 995], True],
        [create_pop_check, ['pop.fakeserver123.com', 995], False],

        [create_imap_check, ['imap.yandex.com', 993], True],
        [create_imap_check, ['imap.fakeserver123.com', 993], False],

        [create_smtp_check, ['aspmx.l.google.com', 25], True],
        [create_smtp_check, ['smtp.fakeserver123.com', 465], False],

        [create_udp_check, ['1.2.3.4', 53, 'uptime.com', 'test'], False],
        [create_udp_check, ['0.north-america.pool.ntp.org', 123, 'c' + 47 * ' ', '$'], True],

        [create_ssh_check, ['ssh.fakeserver123.com'], False],
        [create_ssh_check, ['sdf.org', 22], True],

        [create_dns_check, ['uptime.com', 'ns-1918.awsdns-47.co.uk', '1.2.3.4'], False],
        [create_dns_check, ['ssh.blinkenshell.org', 'ns1.blinkenshell.org', '194.14.45.10'], True],

        # these checks need several hours to run
        [create_rum_check, ['uptime.com'], None],

        [create_blacklist_check, ['uptime.com'], None],
        [create_malware_check, ['uptime.com'], None],

        [create_ssl_check, ['uptime.com'], None],
        [create_ssl_check, ['expired.badssl.com'], None],

        [create_whois_check, ['uptime.com', 30, 'uniregistrar corp'], None],
        [create_whois_check, ['uptime.com', 30, None, ['false-server.com']], None],
    ]


    checks = []
    for fnc, args, status in defs:
        try:
            check = fnc(*args)
            checks.append([check, status])
            print("Created check type: %s, name: %s, id: %s" % (
                check['check_type'], check['name'], check['pk']))
        except Exception as e:
            print("Failed to create check %s %s: %s" % (
                fnc.__name__, args, str(e)))
        time.sleep(10)  # prevent rate limit exception

    wait = 10
    while wait > 0:
        print(f'Waiting {wait} minutes...')
        time.sleep(60)
        wait -= 1

    print("Checking statuses...")
    for check, status in checks:
        if status is None:
            print("Check %d status can only be checked using website" % check['pk'])
            continue

        check = call_api('/checks/%d/' % check['pk'])
        if check['state_is_up'] != status:
            print("Check %d status %s is not as expected %s" % (
                check['pk'], up_or_down(check['state_is_up']), up_or_down(status)))


def parse_args():
    global API_URL, TOKEN, CONTACT_GROUPS, LOCATIONS, TAGS
    parser = argparse.ArgumentParser(description='Create and test all kinds of checks.')
    parser.add_argument('--token', required=True,
                        help='Your Uptime.com API Token')
    parser.add_argument('--contacts', required=True,
                        help='Comma separated list of existing contact groups to assign to checks')
    parser.add_argument('--locations',
                        help='Comma separated list of available locations to assign to checks')
    parser.add_argument('--tags',
                        help='Comma separated list of exiting tags to assign to checks')
    parser.add_argument('--api', default='https://uptime.com/api/v1/',
                        help='(optional) The Uptime.com API endpoint to use, eg. '
                             'https://uptime.com/api/v1/')

    opts = parser.parse_args()
    API_URL = opts.api
    TOKEN = opts.token
    if opts.contacts is not None:
        CONTACT_GROUPS = opts.contacts.split(',')
    if opts.locations is not None:
        LOCATIONS = opts.locations.split(',')
    if opts.tags is not None:
        TAGS = opts.tags.split(',')


if __name__ == '__main__':
    create_checks()
