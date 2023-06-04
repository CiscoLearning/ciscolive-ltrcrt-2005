"""
Module providing core NETCONF configuration functionality for Cisco Live
LTRCRT-2005.

Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Jeremy Cohoe, Palmer Sample, Juulia Santala"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# pylint: disable=broad-exception-caught
import os
import re
from ipaddress import IPv4Interface
from typing import Optional
from ncclient import manager
from ncclient.xml_ import new_ele_ns
from jinja2 import (Environment,
                    FileSystemLoader,
                    select_autoescape)

DEVICE_USERNAME = os.environ.get("DEVICE_USERNAME")
DEVICE_PASSWORD = os.environ.get("DEVICE_PASSWORD")

jinja2_environment = Environment(
    loader=FileSystemLoader(f"{os.path.dirname(__file__)}/templates"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True)

interface_template = jinja2_environment.get_template("configure_interface.xml.j2")


def send_configuration(device_mgmt_ip: str,
                       netconf_payload: str,
                       sync_netconf_db: bool = True,
                       save_config: bool = True):
    """
    Send a NETCONF RPC to the target device. Optionally, sync the running
    config to the NETCONF database and save the config after applying

    :param device_mgmt_ip: Management IP (or hostname) of the target device
    :param netconf_payload: XML payload to send to device
    :param sync_netconf_db: Sync the running config to DB before sending RPC?
    :param save_config: Save the running config after sending RPC?
    :return: None
    """

    with manager.connect(host=device_mgmt_ip,
                         port=830,
                         timeout=30,
                         username=DEVICE_USERNAME,
                         password=DEVICE_PASSWORD,
                         hostkey_verify=False) as nc_session:

        if sync_netconf_db:
            # Force a DB sync before proceeding
            print("Synchronizing running configuration with NETCONF datastore...")
            netconf_sync_payload = new_ele_ns("sync-from", "http://cisco.com/yang/cisco-ia")
            nc_session.dispatch(netconf_sync_payload)

        print(f"Sending payload:\n{netconf_payload}")
        with nc_session.locked("running"):
            nc_session.edit_config(target="running",
                                   config=netconf_payload,
                                   default_operation="merge")
            if save_config:
                print("Saving running-configuration....")
                netconf_save_payload = new_ele_ns("save-config", "http://cisco.com/yang/cisco-ia")
                nc_session.dispatch(netconf_save_payload)


def configure_interface(device_mgmt_ip: Optional[str],
                        template_data: dict):
    """
    Configure an interface using NETCONF

    :param device_name: Name of device to update
    :param interface_name: Interface to update
    :param device_mgmt_ip: NETCONF Management IP address
    :param interface_enabled: Interface state (true=enabled, false=shutdown)
    :param interface_mtu: Max Transmission Unit (1500-9000)
    :param interface_description: Description of interface
    :param interface_mode: Operational mode (access, trunk, or l3)
    :param interface_ipv4: IPv4 Address for L3 interface
    :param untagged_vlan: Untagged (access) or native (trunk) VLAN
    :param tagged_vlans: List of allowed VLANs for trunk interface
    :param ticket_number: If supplied, use to track ITSM change ticket number
    :return: None
    """
    # NETCONF payload requires the interface type and ID. Take interface_name
    # and split into the type and ID.
    interface_regex = re.compile(r"^(\D+)(.*)$")
    interface_type, interface_id = interface_regex.match(template_data["interface_name"]).groups()
    template_data.update({"interface_type": interface_type, "interface_id": interface_id})

    # If there is a ticket number, append to description for future reference
    # if interface_description and ticket_number:
    #     interface_description = f"{interface_description} ##ticket:{ticket_number}##"
    if template_data.get("interface_description") and template_data.get("ticket_number"):
        template_data.update(
            {
                "interface_description": f"{template_data['interface_description']} "
                                         f"##ticket:{template_data['ticket_number']}##"
            }
        )

    # Render the NETCONF RPC template with all values provided
    interface_config = interface_template.render(template_data=template_data)

    # Send the rendered template data to the device
    try:
        mgmt_ip = device_mgmt_ip or template_data["device_mgmt_ip"]
        send_configuration(mgmt_ip,
                           interface_config,
                           sync_netconf_db=True,
                           save_config=True)
    except Exception as err:
        print(f"Error sending the NETCONF payload!\n{err}")
        return_value = False
    else:
        return_value = True

    return return_value


if __name__ == "__main__":

    # If run from CLI, change the path so the "common" package can be loaded.
    import sys
    sys.path.append(f"{os.path.dirname(__file__)}/..")
    from common import get_interface_args

    args = get_interface_args()

    # If there's in IP address, get the IP and netmask.
    # pylint: disable=invalid-name
    if args.interface_ipv4:
        args.interface_ip = str(IPv4Interface(args.interface_ipv4).ip)
        args.interface_netmask = str(IPv4Interface(args.interface_ipv4).netmask)
    else:
        args.interface_ip = None
        args.interface_netmask = None

    # Configure the interface if it's not management-only
    if "1/0/1" in args.interface_name or "1/0/24" in args.interface_name:
        print(f"Unable to configure interface '{args.interface_name}' - "
              "management only.")
    else:
        configure_interface(args.device_name, template_data=vars(args))
