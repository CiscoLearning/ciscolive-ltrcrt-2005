#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Back end code for lab. This is used to create webhooks for Card attachments.
The code presented here can be used as inspiration for webhooks creation,
however it is important to note that the module has been created strictly
the card attachment action use case in mind.

Webex sample function to create and retrieve Webex webhooks using a bot.

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

import os
import requests

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


def create_card_webhook(token, name, pod_number=None):
    '''
    Function to create a webhook to react to card events.
    '''
    if not pod_number:
        pod_number = input("Please enter your pod number: ")
        pod_number.strip()
        if len(pod_number) == 1:
            pod_number = f"0{pod_number}"

    target_url = f"https://pod{pod_number}-webex.{os.environ.get('LAB_DNS_DOMAIN')}:3389/card"
    resource = "attachmentActions"
    event = "created"

    current_webhooks = _get_my_webhooks(token)
    for webhook in current_webhooks["items"]:
        if webhook["targetUrl"] == target_url:
            print(f"A webhook with target URL {target_url} already exist.")
            print("Cannot create a new webhook with the same target URL!")
            return 0

        if webhook["name"] == name:
            print(f"A webhook already exists with the name {name} with following parameters:")
            print(f"- target url {webhook['targetUrl']} (your current request: {target_url})")
            print(f"- resource {webhook['resource']} and event {webhook['event']}", end=" ")
            print(f"your current request: {resource}, {event}")

            question = f"Would you like to create a new webhook {name}_1 with your parameters?"
            selection = input(f"{question} (yes / no) ")
            if selection == "yes":
                name = f"{name}_v1"
            elif selection == "no":
                print("Not creating a webhook!")
                return 0
            else:
                print("Did not understand your input!")
                return 0

    response = _create_webhook(  # pylint: disable=unused-variable
        token=token,
        webhook_name=name,
        webhook_resource=resource,
        webhook_event=event,
        webhook_target_url=target_url
    )
    return 1


# pylint: disable=too-many-arguments
def _create_webhook(token,
                    webhook_name,
                    webhook_resource,
                    webhook_event,
                    webhook_target_url,
                    webhook_filter=None
                    ):
    '''
    Function to create a webhook.
    '''
    print(f"Starting to create Webex webhook: {webhook_name}")

    url = "https://webexapis.com/v1/webhooks"

    headers = {
        "authorization":f"Bearer {token}",
        "Content-Type":"application/json"
    }

    payload = {
        "name":webhook_name,
        "targetUrl":webhook_target_url,
        "resource": webhook_resource,
        "event": webhook_event,
    }

    if webhook_filter:
        payload["filter"] = webhook_filter

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status code of creating the Webex webhook: {response.status_code}")

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")  # pylint: disable=broad-exception-raised

    return response.json()


def _get_my_webhooks(token):
    '''
    Function to get all webhooks of the owner of the token.
    '''
    print("Retrieving webhooks...")
    url = "https://webexapis.com/v1/webhooks"
    headers = {"authorization":f"Bearer {token}"}
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status code of retrieving the Webex webhooks: {response.status_code}")
    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}") # pylint: disable=broad-exception-raised
    return response.json()
