# vCloud Availability Orchestrator Examples
This folder contains a collection of sample vRealize Orchestrator workflows that automate Disaster Recovery Use cases with vCloud Availability.


### Prerequisites

Viewing of workflow examples requires installation of the following products:

* VMware vRealize Orchestrator

Execution of workflow examples requires installation of the following products:

* VMware vRealize Orchestrator

* VMware vCloud Availability installed at a Cloud Provider

* VMware vSphere Replication Appliance 6 installed and registered with a vCenter Server.

## Workflows

![workflows Screenshot](/images/workflows.png "workflows Screenshot")

## Samples

* DR Plan Example

A pair of workflows that enable the creation and execution of a Disaster Recovery plan that assembles replicated virtual machines into prioritized groups and performs failover / test operations on the groups in the cloud in priority order.

* Protect VMs in folder

A workflow that configures replication for all VMs in a specified vcenter folder.  This workflow can be scheduled to run periodically to protect VMs as they are added to the folder.

* Change IP of protected VM

A workflow that changes the IP of a VM after failover. 


## Contributing

The vcloud-availability-examples project team welcomes contributions from the community. If you wish to contribute code and you have not
signed our contributor license agreement (CLA), our bot will update the issue when you open a Pull Request. For any
questions about the CLA process, please refer to our [FAQ](https://cla.vmware.com/faq). For more detailed information,
refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## License
This work is available under the [Apache 2 license](LICENSE).
