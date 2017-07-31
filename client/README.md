

# vcloud-availability-examples

### vclient

A bash script that implements a basic vcd rest client.


### Prerequisites

* Bash shell

### Installation

```git clone https://github.com/vmware/vcloud-availability-examples.git```

```cd vcloud-availability-examples/client```




### Usage

* Run the client without command options for usage:

  ```./vclient```

* Login using the login command 

  ```./vclient login 207.187.188.190 'administrator@system' 'vmpass42' ```

* Get the org uri

  ```xml
./vclient g org 

 <?xml version="1.0" encoding="UTF-8"?>
 <OrgList xmlns="http://www.vmware.com/vcloud/v1.5" href="https://vcd-01a.corp.local/api/org/" type="application/vnd.vmware.vcloud.orgList+xml" 
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vmware.com/vcloud/v1.5 http://vcd-01a.corp.local/api/v1.5/schema/master.xsd">
    <Org href="https://vcd-01a.corp.local/api/org/a93c9db9-7471-3192-8d09-a8f7eeda85f9" name="System" type="application/vnd.vmware.vcloud.org+xml"/>
    <Org href="https://vcd-01a.corp.local/api/org/e46b03d6-46bc-4c95-94fc-27a6c78737a9" name="ACME" type="application/vnd.vmware.vcloud.org+xml"/>
</OrgList>
```

