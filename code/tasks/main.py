from flask import Flask, request
import netconf
import webex
import netbox
import tickets
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
    print(event)

    # Add here the Webex webhook code when asked in the lab guide

    return "Received data!"


@app.route("/netbox", methods=["POST"])
def netbox_webhook():
    '''Function to be used with the NetBox webhook'''

    event = request.json
    print(event)

    return "Received NetBox event!"


@app.route("/ticket", methods=["POST"])
def ticket_webhook():
    '''Function to be used with the ticketing system webhook'''

    event = request.json
    print(event)

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
