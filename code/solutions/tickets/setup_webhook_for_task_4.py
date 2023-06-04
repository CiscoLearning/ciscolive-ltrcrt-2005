"""
A quick helper script for creating the webhook for task 4.

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
# from webex import webex_token
# from netbox_card import create_card_webhook

if __name__ == "__main__":

    # If run from CLI, change the path so the "common" package can be loaded.
    import sys
    sys.path.append(f"{os.path.dirname(__file__)}/..")

    from webex import webex_token
    from netbox_card import create_card_webhook

    create_card_webhook(token=webex_token,
                        name="Cisco Live card",
                        pod_number=os.getenv("PODID") or None)
