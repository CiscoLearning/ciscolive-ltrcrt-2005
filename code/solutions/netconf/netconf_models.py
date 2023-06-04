# pylint: disable=no-self-argument
"""
Model definitions for incoming NETCONF RPC generation based on NetBox data.

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
from pydantic import (BaseModel,  # pylint: disable=no-name-in-module
                      constr,
                      Field,
                      root_validator)


# pylint: disable=too-few-public-methods

INTERFACE_MODE_REGEX = r"^trunk|access|l3$"
ALLOWED_SWITCHPORT_MODES = ("l3", "trunk", "access")


class NetconfWebhookValidator(BaseModel):
    """
    pydantic model to validate NetBox data for XML payload generation
    """
    ticket_number: str
    device_name: str
    interface_name: str = Field(alias="name")
    interface_enabled: bool = Field(alias="enabled", default_factory=True)
    interface_mtu: Optional[int] = Field(alias="mtu", default_factory=1500)
    interface_description: Optional[str] = Field(alias="description", default_factory=None)
    interface_mode: Optional[constr(regex=INTERFACE_MODE_REGEX)] = None
    untagged_vlan: Optional[int] = 1
    tagged_vlans: Optional[list[int]] = []
    interface_ipv4: Optional[str]
    interface_ip: Optional[str] = None
    interface_netmask: Optional[str] = None

    @root_validator(pre=True)
    def extract_values_from_netbox_webhook(cls, values):
        """

        :param values: Root validator values from pydantic
        :return: Validated fields for NETCONF RPC generation
        """
        values["device_name"] = values["device"]["name"]
        values["ticket_number"] = values["custom_fields"]["change_ticket_number"]

        netbox_interface_mode = values["mode"]

        if netbox_interface_mode is None:
            values["interface_mode"] = "l3"

        elif netbox_interface_mode["value"] in ["tagged", "tagged-all", "access"]:
            if values["untagged_vlan"]:
                values["untagged_vlan"] = values["untagged_vlan"]["vid"]
            else:
                values["untagged_vlan"] = 1

            if netbox_interface_mode["value"] in ["tagged", "tagged-all"]:
                values["interface_mode"] = "trunk"

                if values["tagged_vlans"]:
                    vlan_list = [vlan["vid"] for vlan in values["tagged_vlans"]]
                    values["tagged_vlans"] = vlan_list
            else:
                values["interface_mode"] = "access"

        return values


def validate_data(webook_data: dict):
    """
    Wrapper function to validate data against the pydantic model.

    :param webook_data: Incoming dict of received data to validate.
    :returns: Result of calling the parse_obj() method of the BaseModel
    """
    return NetconfWebhookValidator.parse_obj(webook_data)
