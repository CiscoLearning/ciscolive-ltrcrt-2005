#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Back end code for lab. This is used to send and receive cards regarding
NetBox events. The code presented here can be used as inspiration for
card based functions, however it is important to note that the module
has been created strictly the NetBox use case in mind.

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

import json
import requests
import jinja2

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


# pylint: disable=too-many-arguments, broad-exception-caught, broad-exception-raised
def send_netbox_card(token:str,
                     recipient_email:str,
                     card_topic:str,
                     card_subtopic:str,
                     card_description:str,
                     netbox_config:list=(),
                     meta_data:list=(),
                     template:str="card.j2"
                     )->bool:
    '''
    Function to call after an event from Netbox.

    General Params:
    - token: webex bot token
    - recipient_email: the email to which the card is sent 1:1
    - template: the name of the jinja2 template used when generating the card

    Params to fill the card:
    - card_topic: main topic on the top of the card
    - card_subtopic: the lighter color text under the topic
    - card_description: the free form text between topic and details
    - netbox_config: the list with all the key-value pairs that should be listed under description
    - meta_data: the list with all the key-value pairs that recipient should not see, but should be
      present in the webhook message after "approve" button has been clicked

    Both netbox_config and meta_data need to be in format:
        [
            {
                "title": "your title text for the field",
                "value": "the value to be added next to the title on the card"
            }
        ]
    '''

    data_for_the_card = {
        "topic": card_topic,
        "subtopic": card_subtopic,
        "description": card_description,
        "config": netbox_config,
        "hidden_config": meta_data
    }

    try:
        card_payload = _create_card_payload(template=template, card_data=data_for_the_card)
        _send_card(token=token, email=recipient_email, card=card_payload)
        return True
    except Exception as err:
        print(f"Error occurred while sending a NetBox card :\n{err}")
        return False


def netbox_card_attachment_event(token:str, event:dict):
    '''
    Function to call after a Webex attachment action event for Netbox card.

    Params:
    - token: webex bot token
    - event: the dict data sent by the event
   '''
    print("Received a card attachment action...", end=" ")
    card_id = event["data"]["id"]
    card_message_id = event["data"]["messageId"]

    _delete_card(token=token, card_message_id=card_message_id)

    card_data = _get_card_response(token, card_id)
    email = _get_email(token, card_data["personId"])

    if card_data["inputs"]["approved"]:
        print("Button pressed: Accept")
        message = "Your action ✅ `Accept` has been recorded."
        message = f"{message} The automation workflow 🚧 will proceed to deploy the changes."
    else:
        print("Button: Decline")
        message = "Your action ❌ `Decline` has been recorded."
        message = f"{message} The change will 🛑 **not** 🛑 be executed."
    return_value = card_data['inputs']

    _send_message(token=token, email=email,message=message)
    return return_value


def _create_card_payload(template:str, card_data:str):
    '''Create a card payload from Jinja2 template and values from YAML file.'''

    with open(template, encoding="utf-8") as my_template:
        template = jinja2.Template(my_template.read())

    try:
        card = template.render(data=card_data)
        return json.loads(card)
    except Exception as err:
        raise Exception("Card creation failed.") from err


def _send_card(token:str, email:str, card:dict)->None:
    '''
    Function to send a Webex message 1:1 based on an email address.
    '''
    print(f"Sending a card to {email}")
    url = "https://webexapis.com/v1/messages"
    headers = {"authorization":f"Bearer {token}", "Content-Type":"application/json"}
    payload = {
        "toPersonEmail":email,
        "text": "This is an adaptive card",
        "attachments":[card]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status code of sending the Webex message: {response.status_code}")

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")


def _get_card_response(token:str, attachment_id:str):
    '''
    Function to get an attachment based on its ID.
    This function will be used together with the card Webhook.
    '''
    print(f"Retrieving attachment: {attachment_id}")

    url = f"https://webexapis.com/v1/attachment/actions/{attachment_id}"
    headers = {
        "authorization":f"Bearer {token}",
        "Content-Type":"application/json"
    }
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status code of retrieving the Webex card attachment: {response.status_code}")

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")
    return response.json()


def _delete_card(token:str, card_message_id:str)->None:
    '''
    Function to delete a card message.
    '''
    print(f"Deleting card message: {card_message_id}")

    url = f"https://webexapis.com/v1/messages/{card_message_id}"
    headers = {"authorization":f"Bearer {token}"}
    response = requests.delete(url, headers=headers, timeout=30)
    print(f"Status code of deleting the Webex card message: {response.status_code}")
    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")


def _send_message(token:str, email:str, message:str):
    '''
    Function to send a Webex message 1:1 based on an email address.
    '''
    print("Sending response message to the card action...", end=" ")
    url = "https://webexapis.com/v1/messages"
    headers = {
        "authorization":f"Bearer {token}",
        "Content-Type":"application/json"
    }
    payload = {"toPersonEmail":email,"markdown":message}
    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print(f"Status code: {response.status_code}")

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")

    return response.json()


def _get_email(token:str, person_id:str)->str:
    '''
    Function to get person's email based on their Webex personId.
    '''
    print(f"Retrieving email of person: {person_id}")

    url = f"https://webexapis.com/v1/people/{person_id}"
    headers = {"authorization":f"Bearer {token}"}
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status code of retrieving the email: {response.status_code}")

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")
    return response.json()["emails"][0]
