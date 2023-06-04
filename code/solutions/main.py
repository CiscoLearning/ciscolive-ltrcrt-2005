"""
Flask app used to receive and process events from Zammad, NetBox, and Webex.
Developed for Cisco Live session LTRCRT-2005.

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

# pylint: disable=broad-exception-caught
from flask import Flask, request
import webex
import netbox
import tickets
import netconf
import netbox_card


app = Flask(__name__)

@app.route("/")
def hello_message():
    '''Function to print a message in browser.'''
    return "<p>Hello, Cisco Live!</p>"

@app.route("/webex", methods=["POST"])
def webex_webhook():
    '''Function to be used with the Webex webhook'''
    event = request.json
    # print(event)

    message_id = event["data"]["id"]
    message_data = webex.get_message(webex.webex_token, message_id)
    # print(message_data)

    message = message_data["text"]
    # print(message)

    if message[:10] == "Configure:":
        configuration = message[10:].strip()
        print(configuration)
        webex.send_message(webex.webex_token, webex.my_email,
                        f"Configuration requests received: '{configuration}'")

    return "Received data!"

@app.route("/netbox", methods=["POST"])
def netbox_webhook():
    '''Function to be used with the NetBox webhook'''

    event = request.json
    print(event)

    webex.send_message(webex.webex_token, webex.my_email, "Webhook data received from NetBox!")
    webhook_details = event.get("data", {})

    if webhook_details.get("custom_fields", {}).get("change_ticket_number", None):
        try:
            validated_data = netconf.validate_data(webhook_details)
            mgmt_ip = netbox.get_device_mgmt_ipv4(validated_data.device_name)
        except Exception as err:
            webex.send_message(webex.webex_token,
                               webex.my_email,
                               f"There was a problem validating the webhook data:\n{err}")
        else:
            webex.send_message(webex.webex_token,
                               webex.my_email,
                               "Valid data received, configuring the device.")
            if netconf.configure_interface(device_mgmt_ip=mgmt_ip,
                                           template_data=validated_data.dict()):
                webex.send_message(webex.webex_token, webex.my_email, "Device has been configured!")
            else:
                webex.send_message(webex.webex_token,
                                   webex.my_email,
                                   "There was a problem configuring the device, "
                                   "check the Flask output for details.")

            netbox.clear_change_ticket_number_from_interface(validated_data.device_name,
                                                             validated_data.interface_name)
    else:
        print("No ticket number attached to this change, skipping!")
    return "Received NetBox event!"


@app.route("/ticket", methods=["POST"])
def ticket_webhook():
    '''Function to be used with the ticketing system webhook'''

    event = request.json
    print(event)

    webhook_details = event.get("ticket", {})
    ticket_id = webhook_details.get("id")
    ticket_number = webhook_details.get("number")

    try:
        validated_data = netbox_card.validate_data(webhook_details)
    except Exception as err:
        webex.send_message(webex.webex_token,
                           webex.my_email,
                           "There was a problem validating the data for ticket number "
                           f"{ticket_number}:\n{err}")
        tickets.update_ticket(ticket_id=ticket_id,
                              comment="There was a problem processing the ticket. "
                                      f"Details:\n\n{err}",
                              state="attention required")
    else:
        tickets.update_ticket(ticket_id=ticket_id,
                              comment="Your change request has been received "
                                      "and is pending approval.",
                              state="pending approval")

        card_text, card_metadata = netbox_card.create_webex_card_data(validated_data.dict())

        netbox_card.send_netbox_card(token=webex.webex_token,
                                     recipient_email=webex.my_email,
                                     netbox_config=card_text,
                                     meta_data=card_metadata,
                                     template="./netbox_card/card.j2",
                                     card_topic=f"Network change request {ticket_number}",
                                     card_subtopic="Request received to do some things",
                                     card_description="Here's some text to enter")

    return "Received ticket event!"


@app.route("/card", methods=["POST"])
def card_webhook():
    '''Function to be used with the Webex card webhook'''

    netbox_data = None

    def parse_card_data(card_response):
        return {item["title"]: item["value"] for item in card_response}

    event = request.json
    card_data = None
    try:
        card_data = netbox_card.netbox_card_attachment_event(webex.webex_token, event)
    except Exception:
        webex.send_message(webex.webex_token, webex.my_email,
                           "Something went wrong when handling your request...")

    print(f"Card data:\n{card_data}")
    netbox_data = parse_card_data(card_data["config"])
    print(f"Here's the parsed data that's going to NetBox:\n{netbox_data}")
    if card_data["approved"]:
        tickets.update_ticket(ticket_id=netbox_data['ticket_id'],
                              comment="This change was approved and is being processed",
                              state="approved")
        try:
            validated_card_data = netbox.NetboxWebhookValidator.parse_obj(netbox_data)
            print(validated_card_data.dict())
        except ValueError as err:
            webex.send_message(webex.webex_token, webex.my_email,
                               f"Problem with incoming netbox data: {err}")
        else:
            print("Configuring NetBox")
            print(validated_card_data)
            if netbox.configure_interface(**dict(validated_card_data)):
                tickets.update_ticket(ticket_id=netbox_data['ticket_id'],
                                      comment="All configuration tasks have completed. "
                                              "Closing change with result: SUCCESS.",
                                      state="closed")
            else:
                tickets.update_ticket(ticket_id=netbox_data['ticket_id'],
                                      comment="There was a problem configuring the interface. "
                                              "Review the console output, correct, and re-try.",
                                      state="attention required")

    else:
        tickets.update_ticket(ticket_id=netbox_data['ticket_id'],
                              comment="This change has been declined and will now be closed.",
                              state="denied")

    return "Card event received"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12345, debug=True)
