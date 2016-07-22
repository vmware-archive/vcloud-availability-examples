

# vcloud-availability-examples

## Reports

### gen_usage_report.py
Generates usage data that can be used for billing/reporting. 

By default you get: ['Organization', 'TotalReplicatedVMs', 'TotalOrganizationReplicationSize']

Usage:

* Dump data to screen:

  ```python gen_usage_report.py username password vcd_url.vmware.local```

* Export data in JSON format:

  ```python gen_usage_report.py username password vcd_url.vmware.local -o dump.json```

* Export data in CSV format:

  ```python gen_usage_report.py username password vcd_url.vmware.local -o dump.csv --csv```

The ```--skip-ssl-check``` flag can be added to skip the SSL certificate verifcation for self signed certs.
The ```--detail``` flag can be added to get a more detailed view of the data.
