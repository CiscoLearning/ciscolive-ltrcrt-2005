"""
Example script to print operational status of an interface using RESTCONF
on a Cisco IOS XE-based device

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
import re
import json
import requests
from urllib3 import disable_warnings


disable_warnings()

interface_regex = re.compile(r"^(\D+)(.*)$")

DEVICE_USERNAME = os.environ.get("DEVICE_USERNAME")
DEVICE_PASSWORD = os.environ.get("DEVICE_PASSWORD")


def get_interface_data(device_name, interface_name):
    """
    Retrieve operational status of a device interface using RESTCONF.

    :param device_name: Name of device to receive the request
    :param interface_name: Interface to retrieve
    """
    interface_type, interface_id = interface_regex.match(interface_name).groups()
    interface_id = requests.utils.quote(interface_id, safe='')

    headers = {
        "Content-type": "application/yang-data+json",
        "Accept": "application/yang-data+json"
    }
    # pylint: disable-next=line-too-long
    url = f"https://{device_name}/restconf/data/Cisco-IOS-XE-native:native/interface/{interface_type}={interface_id}"

    restconf_data = requests.get(url,
                                 auth=(DEVICE_USERNAME, DEVICE_PASSWORD),
                                 headers=headers, verify=False,
                                 timeout=30)
    print(json.dumps(restconf_data.json(), indent=4))


if __name__ == "__main__":
    from common import get_interface_args
    args = get_interface_args()

    get_interface_data(args.device_name, args.interface_name)
