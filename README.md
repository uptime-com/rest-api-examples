# rest-api-examples
Usage examples for Uptime.com's REST API.


## Powershell

- `add-http-check.ps1`
  Shows how to create a HTTP check with Powershell.
  
- `set-check-under-maintenance.ps1`
  Shows how to set a check under maintenance with Powershell.
  
If using an older version of windows you may need to force TLS 1.2 to use the above scripts:
```
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```
NOTE: This will only change it for the current PowerShell session


## Python
These scripts will run under any recent Python 3 interpreter.
Run these as follows: `python3 script.py --token <YOUR_API_TOKEN>`

- `create_update_http_check.py`
  Shows how to create and update a HTTP check with Python.

- `delete_sample_checks.py`
  Deletes all checks created by these API samples.

- `monitor_checks_and_alerts.py`
  Demonstrates how to monitor the status of checks and alerts in real-time
  without exceeding the API fair use limits.

- `create_and_test_all_checks.py`
  Shows how to create all kinds of checks via the API. This script creates a pair of
  checks with an expected UP/DOWN state for most check types. It waits 10 minutes and
  compares the expected check state to the actual one where possible.
