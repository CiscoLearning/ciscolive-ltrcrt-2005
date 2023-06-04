# pylint: disable=no-self-argument
"""
Model definitions for NetBox webhook data.

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

import ipaddress
from typing import Optional
from pydantic import (BaseModel,  # pylint: disable=no-name-in-module
                      root_validator)


class NetboxWebhookValidator(BaseModel):
    """
    pydantic model to validate data destined for NetBox.
    """

    ticket_number: str
    device_name: str
    interface_name: str
    interface_enabled: bool = True
    interface_mtu: int = 1500
    interface_description: Optional[str] = None
    interface_mode: Optional[str] = None
    untagged_vlan: Optional[int] = None
    tagged_vlans: Optional[list[int]]
    interface_ipv4: Optional[ipaddress.IPv4Interface] = None

    @root_validator(pre=True)
    def convert_tagged_vlans_to_list(cls, values):
        """
        Validator to convert a CSV formatted string of VLAN IDs to a list of
        integers.

        :param values: Root validator values from pydantic
        :returns: Tagged VLANs as a list of integers
        """
        if values["interface_mode"] == "trunk" and values["tagged_vlans"]:
            vlan_list = [int(v) for v in values["tagged_vlans"].split(",")]
            values["tagged_vlans"] = vlan_list
        else:
            values["tagged_vlans"] = []
        return values

    @root_validator(pre=True)
    def convert_ipv4_to_object(cls, values):
        """
        Do not permit invalid interface IPv4 addresses.

        :param values: Root validator values from pydantic
        :returns: Interface IPv4 address as string in CIDR notation
        :raises: ValueError if the IPv4 validation fails
        """
        if values.get("interface_ipv4"):
            try:
                validated_ipv4 = ipaddress.IPv4Interface(values.get("interface_ipv4"))
                values["interface_ipv4"] = str(validated_ipv4)
            except Exception as exc:
                raise ValueError("IPv4 Address must be in CIDR format (a.b.c.d/xy)") from exc

        return values
