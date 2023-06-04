"""
Functions used to process ticket system interaction. Originally created for
Cisco Live session LTRCRT-2005

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
import requests
from zammad_py import ZammadAPI


ticket_url = os.environ.get("TICKET_URL")
ticket_username = os.environ.get("TICKET_USERNAME")
ticket_password = os.environ.get("TICKET_PASSWORD")

ticket_client = ZammadAPI(url=ticket_url,
                          username=ticket_username,
                          password=ticket_password)


def update_ticket(ticket_id: int,
                  comment: str = None,
                  state: str = None):
    """
    Update a ticket with state change or comment.

    :param ticket_id: Ticket ID (not number, the DB ID)
    :param comment: Optional comment to add to the ticket
    :param state: Optional state change for the ticket
    :return: None
    """

    ticket_params = {}
    if state:
        ticket_params.update({"state": state})
    if comment:
        ticket_comment = {
            "body": comment,
            "type": "note",
            "internal": False,
        }
        ticket_params.update({"article": ticket_comment})

    print(f"\nUpdating ticket with parameters: {ticket_params}")
    if ticket_params:
        try:
            ticket_client.ticket.update(id=ticket_id, params=ticket_params)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error encountered: {err}")
