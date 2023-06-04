# pylint: disable=no-self-argument
"""
Model definitions for Webex cards based on NetBox data.

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

from typing import Optional
import ipaddress
import json
from pydantic import (BaseModel,  # pylint: disable=no-name-in-module
                      constr,
                      Field,
                      root_validator)

# pylint: disable=too-few-public-methods

INTERFACE_MODE_REGEX = r"^trunk|access|l3$"
ALLOWED_SWITCHPORT_MODES = ("l3", "trunk", "access")

webex_card_field_descriptions = {
    "ticket_number": "Change ticket",
    "device_name": "Device",
    "interface_name": "Interface",
    "interface_enabled": "Enabled?",
    "interface_description": "Description",
    "interface_mtu": "MTU",
    "interface_mode": "Mode",
    "untagged_vlan": "Native VLAN",
    "tagged_vlans": "Allowed VLANs",
    "interface_ipv4": "IPv4 address"
}


class NetboxCardWebhookValidator(BaseModel):
    """
    pydantic model to validate ticket data for Webex cards
    """

    ticket_id: int = Field(alias="id")
    ticket_number: str = Field(alias="number")
    device_name: str = Field(alias="network_device_name")
    interface_name: str = Field(alias="network_interface_name")
    interface_enabled: Optional[bool] = Field(alias="network_interface_enabled",
                                              default_factory=True)
    interface_mtu: int = Field(alias="network_interface_mtu",
                               default_factory=1500)
    interface_description: Optional[str] = Field(alias="network_interface_description",
                                                 default_factory=None)
    interface_mode: Optional[constr(regex=INTERFACE_MODE_REGEX)] = None
    untagged_vlan: Optional[int] = None
    tagged_vlans: Optional[list[int]] = []
    interface_ipv4: Optional[str]

    # pylint: disable=raise-missing-from
    @root_validator(pre=True)
    def get_interface_mode_and_vlans(cls, values):
        """
        Parse interface mode (access, trunk, l3) and VLANs to be send in
        Webex approval cards for NetBox updates.

        :param values: Root validator values from pydantic
        :return: Validated fields for interface mode and VLANs
        :raises: ValueError on data validation error
        """
        try:
            switchport_mode, native_vlan, tagged_vlans = \
                values["network_switchport_mode_and_vlan"].split(":")
            if switchport_mode not in ALLOWED_SWITCHPORT_MODES:
                switchport_mode = None
        except ValueError:
            raise ValueError(
                "Invalid switchport mode selected. "
                "Only 'Not Defined', 'Access', 'Trunk', or 'L3' are permitted.")

        values["interface_mode"] = switchport_mode
        if switchport_mode == "l3":
            try:
                validated_address = ipaddress.IPv4Interface(
                    values["network_interface_ip4_address"]
                )
                if validated_address.network.prefixlen == 32:
                    raise ValueError("IPv4 prefix length must be less than "
                                     "/32 for interface assignment.")
                values["interface_ipv4"] = str(validated_address)
            except ipaddress.AddressValueError:
                raise ValueError("Invalid IPv4 address supplied. "
                                 "Address must be in CIDR format (a.b.c.d/xy)")

        if native_vlan:
            values["untagged_vlan"] = int(native_vlan)
        if tagged_vlans:
            values["tagged_vlans"] = [int(v) for v in tagged_vlans.split(",")]
        return values


def validate_data(webook_data: dict):
    """
    Wrapper function to validate data against the pydantic model.

    :param webook_data: Incoming dict of received data to validate.
    :returns: Result of calling the parse_obj() method of the BaseModel
    """
    return NetboxCardWebhookValidator.parse_obj(webook_data)


def create_webex_card_data(ticket_data: dict):
    """
    Given a dict of validated data, use the webex_card_field_descriptions
    to generate a human-friendly dict for the Webex card, as well as the
    metadata that will actually be returned on card accept/reject.

    :param ticket_data: Validated ticket data dict
    :return: Tuple of human-friendly dict and metadata for Card return values
    """
    # pylint: disable=invalid-name

    card_metadata = []
    card_text = []
    for k, v in ticket_data.items():

        if isinstance(v, list):
            v = ", ".join(str(x) for x in v)
        card_metadata.append(
            {
                "title": k,
                "value": json.dumps(v)
            }
        )

        if v is None or v == []:
            v = "-"
        if k in webex_card_field_descriptions:
            card_text.append(
                {
                    "title": webex_card_field_descriptions[k],
                    "value": "-" if v is None or v == [] else v
                }
            )

    return card_text, card_metadata
