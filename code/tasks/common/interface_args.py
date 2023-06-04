"""
Importable module to provide common arguments for Python scripts designed
to interact with network devices via automation interfaces.

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

from argparse import (ArgumentParser,
                      RawDescriptionHelpFormatter,
                      ArgumentTypeError)
from os.path import basename
from ipaddress import IPv4Interface


ALLOWED_UNTAGGED_VLANS = (1, 100, 200, 300, 400, 500)
ALLOWED_TAGGED_VLANS = (100, 200, 300, 400, 500)
MIN_MTU = 1500
MAX_MTU = 9000

example_usage = f"""

-----------------------------------------------------------------------------
Example usage:
    python {basename(__file__)} -d sw2 -i "GigabitEthernet1/0/3" -e --desc "Uplink to access-rtr1" access -u 100
        Enable interface GigabitEthernet1/0/3 on device sw2 as an access
        port on VLAN 100 with description "Uplink to access-rtr1"

    python {basename(__file__)} -d sw3 -i "GigabitEthernet1/0/19" -e --desc "esxi-01 vmnic2" trunk -u 100 -t 300,400
        Enable interface GigabitEthernet1/0/19 on device sw3 as a trunk
        port with native VLAN 100 and tagged VLANs 300 and 400 with
        description "esxi-01 vmnic2"

    python {basename(__file__)} -d core-rtr1 -i GigabitEthernet2 -s
        Shutdown interface GigabitEthernet2 on device core-rtr1

    python {basename(__file__)} -d c9300 -i Loopback100 --desc "NTP Source Interface"
        Set the description for interface Loopback100 on device c9300 to
        "NTP Source Interface"

You can also split long lines using the standard '\\' separator:

    python {basename(__file__)} -d sw3 -i "GigabitEthernet1/0/19" -e \\
        --desc "esxi-01 vmnic2" trunk -u 100 -t 300,400

"""


def get_interface_args():
    """
    Function to define common args for scripts running in __main__.

    :returns: Object returned from argparse.Argumentparser.parse_known_args()
    """

    def allowed_mtu(arg):
        mtu = int(arg)
        if not MIN_MTU <= mtu <= MAX_MTU:
            raise ArgumentTypeError(f"Invalid MTU '{mtu}'. Allowed MTU range "
                                    f"is {MIN_MTU} - {MAX_MTU}")
        return mtu

    def vlan_id_choices(choices):
        """
        Validate provided CSV-formatted string of VLANs against a list of
        allowed VLANs.

        :param choices: Allowed VLAN IDs to validate
        :returns: Result of the tagged_vlan validation function
        """

        def tagged_vlan(arg):
            """
            Given a CSV-formatted string of VLAN IDs, split and cast each ID
            as an int.

            :param arg: Argument passed on comand line
            :return: List of int containing validated VLAN IDs
            :raises: ArgumentTypeError if provided VLAN is not allowed
            """
            values = [int(v) for v in arg.split(',')]
            for value in values:
                if value not in choices:
                    raise ArgumentTypeError(f"Invalid tagged VLAN '{value}' - "
                                            f"supported VLANs are {choices}")
            return values
        return tagged_vlan

    parser = ArgumentParser(description="Set configuration parameters for an"
                                        "interface on a device. See 'Example "
                                        "usage' below for more information.",
                            epilog=example_usage,
                            formatter_class=RawDescriptionHelpFormatter)

    parser.set_defaults(interface_enabled=None,
                        interface_mode=None,
                        interface_mtu=None,
                        untagged_vlan=None,
                        tagged_vlans=[],
                        interface_ipv4=None,
                        management_ip=None)

    parser.add_argument("-d",
                        action="store",
                        dest="device_name",
                        required=True,
                        help="Device to configure")
    parser.add_argument("-i",
                        action="store",
                        dest="interface_name",
                        required=True,
                        help="Interface to configure. "
                             "Recommended to enclose the value in quotes "
                             "(e.g. \"GigabitEthernet1/0/1\" or \"Loopback100\")")
    interface_state_group = parser.add_mutually_exclusive_group()
    interface_state_group.add_argument("-e",
                                       action="store_true",
                                       dest="interface_enabled",
                                       help="Enable interface ('no shutdown'). "
                                            "This is the default if not specified.")

    interface_state_group.add_argument("-s",
                                       action="store_false",
                                       dest="interface_enabled",
                                       help="Disable interface ('shutdown').")

    parser.add_argument("-m",
                        action="store",
                        dest="interface_mtu",
                        default=None,
                        type=allowed_mtu,
                        help="Interface MTU. Default: 1500")
    parser.add_argument("-desc", "--desc",
                        action="store",
                        dest="interface_description",
                        default=None,
                        help="Description for target interface. Enclose in quotes "
                             "(e.g. \"This is an interface description\"). Default: None")

    root_iface_mode_parser = parser.add_subparsers(title="Interface mode")
    access_mode_parser = root_iface_mode_parser.add_parser("access")
    access_mode_parser.set_defaults(interface_mode="access")
    access_mode_parser.add_argument("-u",
                                    action="store",
                                    dest="untagged_vlan",
                                    default=1,
                                    type=int,
                                    choices=ALLOWED_UNTAGGED_VLANS,
                                    help="Access VLAN ID. Default: 1")

    trunk_mode_parser = root_iface_mode_parser.add_parser("trunk")
    trunk_mode_parser.set_defaults(interface_mode="trunk")
    trunk_mode_parser.add_argument("-u",
                                    action="store",
                                    dest="untagged_vlan",
                                    default=1,
                                    type=int,
                                    choices=ALLOWED_UNTAGGED_VLANS,
                                    help="Trunk native VLAN ID. Default: 1")
    trunk_mode_parser.add_argument("-t",
                                   action="store",
                                   dest="tagged_vlans",
                                   default=[],
                                   metavar=f"{{[{str(ALLOWED_TAGGED_VLANS).replace(' ', '')}]}}",
                                   type=vlan_id_choices(ALLOWED_TAGGED_VLANS),
                                   help="Tagged VLANs for trunk port, separated by commas "
                                        "(e.g. 100,200,400). Ignored for access port. "
                                        "Default: None")

    l3_mode_parser = root_iface_mode_parser.add_parser("l3")
    l3_mode_parser.set_defaults(interface_mode="l3")
    l3_mode_parser.add_argument("-ip", "--ip",
                                action="store",
                                dest="interface_ipv4",
                                default=None,
                                type=IPv4Interface,
                                help="IPv4 Address in CIDR notation for L3 interface. "
                                     "Quotes recommended (e.g. \"192.168.1.1/24\")",
                                required=True)

    interface_args, _ = parser.parse_known_args()
    return interface_args
