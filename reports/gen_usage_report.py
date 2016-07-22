#!/usr/bin/env python
"""
This script generates a usage report from the vCloud Director API.

“Copyright © 2016 VMware, Inc. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the “License”); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at http://www.apache.org/licenses/LICENSE-2.0
Some files may be comprised of various open source software components, each of which
has its own license that is located in the source code of the respective component."

"""
import argparse
import csv
import json
import requests
import xml.etree.ElementTree as ET

from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#Hide warning when we are skipping the SSL verification check.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
HEADERS = {'Accept' : 'application/*+xml;version=6.0'}
VERIFY_CERT = True

#Login
def vcd_login(username, password, url):
    """
    Perform login to vCloud Director, saving the vcloud auth token to header.
    """

    response = requests.post(url + "sessions", headers=HEADERS,
                             auth=(username, password), verify=VERIFY_CERT)

    if response.status_code == requests.codes.OK:
        HEADERS["x-vcloud-authorization"] = response.headers.get('x-vcloud-authorization')
    else:
        print "ERROR: There was an error logging into vCloud Director."
        print "STATUS: %s \n\n %s" % (response.status_code, response.content)
        exit()


def vcd_get(url):
    """
    Generic call that will be used for all HTTP GET calls.
    """

    response = requests.get(url, headers=HEADERS, verify=VERIFY_CERT)

    if response.status_code == requests.codes.OK:
        try:
            return ET.fromstring(response.content)
        except Exception as err:
            print "ERROR - Unable to convert response from %s to XML" % url
            print err
            exit()
    else:
        print "ERROR - GET call to %s returned:" % url
        print "STATUS: %s" % response.status_code
        return None

def get_orgs(url):
    """
    Return a dict of organizations in vCloud Director.
    """

    orgs = {}

    org_list = vcd_get(url + "org")

    for org in org_list:
        orgs[org.attrib['name']] = org.attrib['href']

    return orgs

def fix_ns(tag):
    """
    A quick hack to clean out the namespace in XML.
    """

    return tag.split('}')[1]

def process_children(element):
    """
    Recursiviely walk XML and return results in dict.
    """

    if list(element):
        ret_data = {}

        for child in list(element):
            ret_data[fix_ns(child.tag)] = process_children(child)

        return ret_data
    else:
        return element.text

def process_detail(href):
    """
    Return dict of replication details.
    Computes TotalVMReplicationSize as a helper.
    """
    
    repl_detail = {'Disks':[], 'TotalVMReplicationSize': 0}

    replication_detail = vcd_get(href)
    if replication_detail is not None:
        for repd in replication_detail:
            replicated_data_size = 0

            if repd.tag.endswith('Vm'):
                for vmd in list(repd):
                    child_tag = fix_ns(vmd.tag)
                    if child_tag == 'Disk':
                        disk_detail = process_children(vmd)
                        replicated_data_size += int(disk_detail['SpaceRequirement'])

                        repl_detail['Disks'].append(disk_detail)
                    else:
                        repl_detail[child_tag] = process_children(vmd)

            repl_detail['TotalVMReplicationSize'] = replicated_data_size

    return repl_detail

def get_replications(orgs):
    """
    Return a dict of all the replicated VMs.
    """

    repl_info = {}

    for key, url in orgs.iteritems():
        if key != "System":
            # Creating Dict to allow for expansion of Organization data.
            repl_info[key] = {'ReplicatedVMs':[], 'TotalOrganizationReplicationSize': 0}

            # ISSUE #2 Consider using grequests module to speed up preformance.
            get_data = True
            page_num = 1
            while get_data:
                replication_references = vcd_get(url+"/replications?page=%s" % page_num)
                total_vms = int(replication_references.attrib['total'])
                page_size = int(replication_references.attrib['pageSize'])

                for reference in replication_references:
                    if reference.tag.endswith('Reference'):
                        repl_data = {'Detail': {}}

                        replication_group = vcd_get(reference.attrib['href'])
                        repl_data['Name'] = replication_group.attrib['name']
                        repl_data['Id'] = replication_group.attrib['id']

                        for el_rg in replication_group:
                            if el_rg.tag.endswith('Link') and el_rg.attrib['rel'] == 'down:details':
                                repl_data['Detail'] = process_detail(el_rg.attrib['href'])

                            elif not el_rg.tag.endswith('Link'):
                                repl_data[fix_ns(el_rg.tag)] = process_children(el_rg)

                        repl_info[key]['TotalOrganizationReplicationSize'] += repl_data['Detail'].get('TotalVMReplicationSize', 0)
                        repl_info[key]['ReplicatedVMs'].append(repl_data)

                if (page_size * page_num) < total_vms:
                    page_num += 1
                else:
                    get_data = False

    return repl_info

def main():
    """
    Main function executed when script is run.
    """

    parser = argparse.ArgumentParser(description='Gather usage data from the vCD-SP API.')
    parser.add_argument('username', help='vCloud Director System user.')
    parser.add_argument('password', help='Provide the password for the System user.')
    parser.add_argument('vcdaddress',
                        help='The URL of the vCloud Director Instance. Example: vcd.vmware.com')
    parser.add_argument('--skip-ssl-check', help='Skip SSL verification.', action='store_false')
    parser.add_argument('-o', '--output', help='Write data to file. Defualt is JSON format.')
    parser.add_argument('--csv', help='Write output in csv instead of JSON', action='store_true')
    parser.add_argument('--detail', help='Output a detailed view', action='store_true')

    args = parser.parse_args()

    vcd_url = "https://%s/api/" % args.vcdaddress

    #Set as global so we don't have to pass around.
    global VERIFY_CERT 
    VERIFY_CERT = args.skip_ssl_check

    vcd_login("%s@System" % args.username, args.password, vcd_url)

    vcloud_orgs = get_orgs(vcd_url)

    vcloud_repl_information = get_replications(vcloud_orgs)

    # If we only want the summary, dump the rest of the data.
    if not args.detail:
        vcloud_repl_information = [(key,
                                    len(repl_data['ReplicatedVMs']),
                                    repl_data['TotalOrganizationReplicationSize'])
                                   for key, repl_data in vcloud_repl_information.iteritems()]

    if args.output:
        print "Output saved to: %s" % args.output
        with open(args.output, 'w') as outfile:
            if args.csv:
                writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

                if not args.detail:
                    writer.writerow(['Organization', 'TotalReplicatedVMs',
                                     'TotalOrganizationReplicationSize'])
                    writer.writerows(vcloud_repl_information)
                else:
                    writer.writerow(['Organization', 'Name', 'Id', 'RecoveryState',
                                     'TestRecoveryState', 'CurrentRpoViolation', 'Paused',
                                     'ReplicationState', 'Rpo', 'TotalVMReplicationSize'])
                    for key, repl_data in vcloud_repl_information.iteritems():
                        writer.writerows([(key, rd['Name'], rd['Id'],
                                           rd['RecoveryState'], rd['TestRecoveryState'],
                                           rd['CurrentRpoViolation'], rd['Paused'],
                                           rd['ReplicationState'], rd['Rpo'],
                                           rd['Detail']['TotalVMReplicationSize'])
                                          for rd in repl_data['ReplicatedVMs']])

            else:
                # Write output in JSON to file.
                json.dump(vcloud_repl_information, outfile)
    else:
        # Dump data to screen.
        pprint(vcloud_repl_information)

if __name__ == '__main__':
    main()

