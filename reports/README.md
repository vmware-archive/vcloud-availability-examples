

# vcloud-availability-examples

## Reports

### gen_usage_report.py
A python script that generates vcloud Availability usage data for billing/reporting. 

Ths script collects the storage usage of replicated virtual machines in a vCD organization, regardless of their replication state (replicated (stopped), replicated test (running), failed over (running or stopped).
The output includes data for all replication enabled virtual data centers in the Orgzanization.

### Prerequisites

* python 2 (minimum 2.7 Not python 3)
* pip      (included in Python 2.7.9 and greater)
* additional python modules installed using pip: requests, yarg, docopt, pipreqs

### Usage

* Dump data to screen:

  ```python gen_usage_report.py username password vcd_url.vmware.local```

* Export data in JSON format:

  ```python gen_usage_report.py username password vcd_url.vmware.local -o dump.json```

* Export data in CSV format:

  ```python gen_usage_report.py username password vcd_url.vmware.local -o dump.csv --csv```

### Example

```python gen_usage_report.py root mypassword  10.162.102.164 ```

### Output 

Default output is: ['Organization', 'TotalReplicatedVMs', 'TotalOrganizationReplicationSize']

* Organization: The name of an organization in the vCloud Director instance.
* TotalReplicatedVMs: A count of the virtual machines that are replicated within all the virtual data centers of the organization.
* TotalOrganizationReplicationSize: A count of total bytes of vmdk storage used by all replicaton VMs.

If more than one Organization exists, the output array contains one entry for each organization.

For example
```[('tenant-org', 0, 0), ('vcenter-1-org', 2, 760225792)]```



### Notes

The ```--skip-ssl-check``` flag can be added to skip the SSL certificate verifcation for self signed certs.

The ```--detail``` flag can be added to get a more detailed view of the data.

Do not include the @system domain as a username suffix, it is automatically added.
