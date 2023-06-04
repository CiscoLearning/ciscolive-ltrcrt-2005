#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Webex sample function to send and retrieve messages using a bot.

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

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests

# pylint: disable=broad-exception-raised

def send_message(token, email, message):
    '''
    Function to send a Webex message 1:1 based on an email address.
    '''
    print(f"Sending message: {message}")

    url = "https://webexapis.com/v1/messages"

    headers = {
        "authorization":f"Bearer {token}",
        "Content-Type":"application/json"
    }

    payload = {
        "toPersonEmail":email,
        "markdown":message
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print(f"Status code of sending the Webex message: {response.status_code}")

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")

    return response.json()


def get_message(token, message_id):
    '''
    Function to get a message based on its ID.
    This function will be used together with the Webhook.
    '''
    print(f"Retrieving message: {message_id}")

    url = f"https://webexapis.com/v1/messages/{message_id}"

    headers = {
        "authorization":f"Bearer {token}",
        "Content-Type":"application/json"
    }

    response = requests.get(url, headers=headers, timeout=30)

    print(f"Status code of retrieving the Webex message: {response.status_code}")

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")

    return response.json()


if __name__ == "__main__":
    from config import webex_token, my_email  # pylint: disable=import-error
    sent = send_message(webex_token, my_email, "Hello Cisco Live!")
    retrieved = get_message(webex_token, sent["id"])
    print(retrieved)
