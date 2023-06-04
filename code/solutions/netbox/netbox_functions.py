"""
Functions used to process NetBox interface changes.

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

import os
from typing import Optional
from ipaddress import IPv4Interface, AddressValueError
import pynetbox
# pylint: disable=broad-exception-caught

nb = pynetbox.api(url=os.environ.get("NETBOX_URL"),
                  token=os.environ.get("NETBOX_TOKEN"))


def get_device_mgmt_ipv4(device_name: str):
    """
    Given a device name, retrieve the primary IPv4 address if present.

    :param device_name: Name of the device in NetBox
    :return: CIDR formatted string of the mgmt IPv4 address or None if DNP
    """
    netbox_device = nb.dcim.devices.get(device=device_name)
    try:
        mgmt_ipv4 = IPv4Interface(netbox_device.primary_ip4.address)
    except AddressValueError:
        print("Unable to get device management IPv4 address")
        mgmt_ipv4 = None
    else:
        mgmt_ipv4 = str(mgmt_ipv4.ip)
    return mgmt_ipv4


def get_netbox_interface(device_name: str,
                         interface_name: str):
    """
    Retrieve the NetBox object for the requested interface on a device.

    :param device_name: Name of the device
    :param interface_name: Name of the interface to retrieve
    :return: NetBox interface object reference
    """
    nb_result = nb.dcim.interfaces.get(device=device_name, name=interface_name)
    return nb_result


def clear_change_ticket_number_from_interface(device_name: str,
                                              interface_name: str):
    """
    Remove any value for the change_ticket_number custom field on an interface.

    :param device_name: Name of the device with the target interface
    :param interface_name: Name of the interface to update
    :return: None
    """
    nb_interface = get_netbox_interface(device_name=device_name,
                                        interface_name=interface_name)
    nb_interface.custom_fields["change_ticket_number"] = None
    nb.dcim.interfaces.update([nb_interface])


def get_netbox_vlan(vlan_id: int):
    """
    Given a VLAN ID, retrieve the NetBox object

    :param vlan_id: VLAN ID to retrieve
    :return: NetBox VLAN object reference (None if no match)
    """
    return nb.ipam.vlans.get(vid=vlan_id)


def get_ip_addresses_for_interface(nb_interface_object: pynetbox.models.dcim.Interfaces,
                                   address_family: int = 4):
    """
    Query NetBox for any IP addresses assigned to the provided interface

    :param nb_interface_object: NetBox interface object reference
    :param address_family: 4 or 6 for IPv4 or IPv4 AF. Default: 4
    :return: RecordSet object with query result
    """
    return nb.ipam.ip_addresses.filter(interface_id=nb_interface_object.id,
                                       family=address_family)


def remove_interface_ip_addresses(nb_interface_object: pynetbox.models.dcim.Interfaces):
    """
    Disassociate any IP addresses from the given NetBox interface object.
    This will *not* delete the IP address or mark it inactive.

    :param nb_interface_object: NetBox interface object reference
    :return: None
    """
    interface_ips = get_ip_addresses_for_interface(nb_interface_object)
    for ip_address in interface_ips:
        ip_address.assigned_object_type = None
        ip_address.assigned_object_id = None
        nb.ipam.ip_addresses.update([ip_address])


def configure_access_port(nb_interface_object: pynetbox.models.dcim.Interfaces,
                          access_vlan: int):
    """
    Given a NetBox interface object and access VLAN, update the object
    'mode' attribute to 'access' and set the untagged VLAN to the
    NetBox ID for the requested VLAN.

    :param nb_interface_object: NetBox interface object reference
    :param access_vlan: Requested access VLAN ID
    :return: None
    :raises: ValueError if NetBox VLAN does not exist
    """
    netbox_vlan = get_netbox_vlan(access_vlan)
    if netbox_vlan:
        nb_interface_object.mode = "access"
        nb_interface_object.untagged_vlan = netbox_vlan
    else:
        raise ValueError("Requested VLAN ID does not exist in NetBox, "
                         "unable to update.")


def configure_trunk_port(nb_interface_object: pynetbox.models.dcim.Interfaces,
                         native_vlan: int,
                         allowed_vlans: list[int]):
    """
    Given a NetBox interface object, native VLAN ID, and a list of allowed
    VLANs, update the object 'mode' attribute to 'trunk', set the untagged
    VLAN to the NetBox ID for native_vlan, and the tagged VLANs to the
    NetBox IDs for the allowed_vlans.

    :param nb_interface_object: NetBox interface object reference
    :param native_vlan: Requested native VLAN ID
    :param allowed_vlans: Requested tagged VLAN IDs
    :return: None
    :raises: ValueError if native or tagged VLAN does not exist in NetBox
    """
    netbox_tagged_vlans = []
    netbox_native_vlan = get_netbox_vlan(native_vlan)

    if not netbox_native_vlan:
        raise ValueError(f"The native VLAN {native_vlan} does not exist "
                         "in NetBox. Unable to update.")

    for vlan in allowed_vlans:
        netbox_vlan = get_netbox_vlan(vlan)
        if netbox_vlan:
            netbox_tagged_vlans.append(netbox_vlan)
        else:
            raise ValueError(f"Requested tagged VLAN {vlan} does not exist "
                             "in NetBox. Unable to update.")

    nb_interface_object.mode = "tagged"
    nb_interface_object.untagged_vlan = netbox_native_vlan
    nb_interface_object.tagged_vlans = netbox_tagged_vlans


def configure_l3_port_ipv4(nb_interface_object: pynetbox.models.dcim.Interfaces,
                           ipv4_address: IPv4Interface):
    """
    Given a NetBox interface object and an IPv4 address,
    check that the provided IP is created and unassigned.

    If not created, create the IP and assign to the interface.
    If created and unassigned, assign to the interface.
    If created and assigned, raise (something)?

    :param nb_interface_object: NetBox interface object reference
    :param ipv4_address: IPv4 address for switch L3 interface
    :return: None
    :raises: ValueError if
    """

    # 1. Check for a different interface in the same network on this device
    for assignment in nb.ipam.ip_addresses.filter(device=nb_interface_object.device.name,
                                                  parent=str(ipv4_address.network),
                                                  family=4,
                                                  assigned_object_type="dcim.interface"):
        if assignment.assigned_object != nb_interface_object:
            raise ValueError("Another interface has an IP in the same network. Cannot assign!")

    # No conflict. Even if the interface has an address assigned, do as instructed
    # in the approved change ticket.

    # 2. Remove any assigned addresses
    remove_interface_ip_addresses(nb_interface_object)

    # 3. Create the parent prefix if it does not exist
    if len(nb.ipam.prefixes.filter(prefix=str(ipv4_address.network))) == 0:
        # The prefix does not exist, create it.
        nb.ipam.prefixes.create(prefix=str(ipv4_address.network),
                                tenant=nb_interface_object.device.tenant.id,
                                site=nb_interface_object.device.site.id,
                                role={"slug": "developer-networks"},
                                description="Created by Python")

    # 4. Create the IP address and assign to the interface if it does not exist
    if len(nb.ipam.ip_addresses.filter(address=str(ipv4_address))) == 0:
        nb.ipam.ip_addresses.create(address=str(ipv4_address),
                                    tenant=nb_interface_object.device.tenant.id,
                                    assigned_object_id=nb_interface_object.id,
                                    assigned_object_type="dcim.interface")
    else:
        # The IP exists in IPAM, now assign to the interface
        netbox_ip_object = nb.ipam.ip_addresses.get(address=str(ipv4_address))
        netbox_ip_object.tenant = nb_interface_object.device.tenant.id
        netbox_ip_object.assigned_object_id = nb_interface_object.id
        netbox_ip_object.assigned_object_type="dcim.interface"
        nb.ipam.ip_addresses.update([netbox_ip_object])

    nb_interface_object.untagged_vlan = None
    nb_interface_object.tagged_vlans = []

    nb_interface_object.mode = ""


# pylint: disable=too-many-arguments, too-many-branches
def configure_interface(device_name: str,
                        interface_name: str,
                        interface_enabled: bool = True,
                        interface_mtu: Optional[int] = None,
                        interface_description: Optional[str] = None,
                        interface_mode: Optional[str] = None,
                        interface_ipv4: Optional[IPv4Interface] = None,
                        untagged_vlan: Optional[int] = 1,
                        tagged_vlans: list[int] = (),
                        ticket_number: Optional[int] = None):
    """
    Update interface details in NetBox

    :param device_name: Name of device to update
    :param interface_name: Interface to update
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

    # Step 1: Retrieve interface object from NetBox
    nb_interface = get_netbox_interface(device_name, interface_name)

    if not nb_interface:
        # The requested interface does not exist on this device.
        raise ValueError("No matching interface found in NetBox for this device.")

    if nb_interface.mgmt_only:
        # Don't update the management interface
        raise ValueError("Interface is management only - cannot update.")

    # Step 2: Set state, MTU, and description for the interface if provided
    if interface_enabled is not None:
        nb_interface.enabled = interface_enabled

    if interface_mtu is not None:
        nb_interface.mtu = interface_mtu

    if interface_description is not None:
        nb_interface.description = interface_description

    # Step 3: Determine the requested interface mode (if supplied)
    try:
        if interface_mode in ["access", "trunk"]:
            # If this is an access or trunk interface, remove any assigned IP
            if nb_interface.count_ipaddresses > 0:
                remove_interface_ip_addresses(nb_interface)

            # Configure access interface
            if interface_mode == "access":
                print("Configuring access interface")
                configure_access_port(nb_interface_object=nb_interface,
                                      access_vlan=untagged_vlan)

            # Configure trunk interface
            elif interface_mode == "trunk":
                print("Configuring trunk interface")
                configure_trunk_port(nb_interface_object=nb_interface,
                                     native_vlan=untagged_vlan,
                                     allowed_vlans=tagged_vlans)

        # Configure L3 interface
        elif interface_mode == "l3":
            print("Configuring L3 interface")
            configure_l3_port_ipv4(nb_interface_object=nb_interface,
                                   ipv4_address=interface_ipv4)

        else:
            print("\tNo interface mode selected, skipping.")

        if ticket_number:
            nb_interface.custom_fields["change_ticket_number"] = ticket_number
        nb.dcim.interfaces.update([nb_interface])
    except Exception:
        configure_result = False
    else:
        configure_result = True

    return configure_result


if __name__ == "__main__":
    # If running from the commandline, ensure the parent directory is included
    # in PYTHONPATH so the common args module can be imported
    import sys
    sys.path.append("../")
    from common import get_interface_args
    args = get_interface_args()

    configure_interface(device_name=args.target_device,
                        interface_name=args.target_interface,
                        interface_mtu=args.interface_mtu,
                        interface_mode=args.interface_mode,
                        interface_description=args.interface_description,
                        interface_enabled=args.interface_enabled,
                        untagged_vlan=args.untagged_vlan,
                        tagged_vlans=args.tagged_vlans,
                        interface_ipv4=args.interface_ipv4)
