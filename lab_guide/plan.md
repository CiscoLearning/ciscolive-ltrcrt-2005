# Notes for Juulia, Palmer, and Jeremy while working on the lab guide

(Solve your first ticket -> Review the ticket and plan your MVP --> Put to slides (interactive discussion to start the session))

**!! Plan !!**
- 15min intro
- 4x 40min hands on + 4x 10min review
- 15min break
- 10min outro

"Configure any interface with any device and learn how to build the event driven flow to it"

------

### 1. Setup for your events: YANG model payload and RESTCONF URL for configuration change (40min)
- Ticket number 1: VLANS
  - First part: run directly from YANG suite
- Ticket number 2: interface config
  - Second part: Jinja2 template based on YANG model
  - Third part: Python script to populate stuff (a module!)
 
### 2. Add an event: Webex bot and deploy Webex Webhook for alerts (40min)
- **Add the next feature! Run again YANG stuff, but send a message**

- FLASK (small section) -> "step 1. review code and `run flask --autoreload` "
  - auto reload
  - code already there to listen for webhook
- Module
  - Get messages
  - Post messages

### 3. Add an event: NetBox for source of truth (40min)
- **Add the next feature! Run again YANG stuff, but get the data from Netbox AND send a message**

- network change will happen
- maybe add vault as well?
- webex message

### 4. Add an event: Ticket system as the source of whateva (40min)
- **Add the final feature for your MVP!  Run again YANG stuff, but get the data from Netbox AND send a message AND close the ticket after asking confirmation in Webex**

- communicate to netbox
- webex message

### [BONUS] Expand the features of your MVP
Bonus 1: Handle your secrets better with Vault<br>
Bonus 2: Interact with a monitoring system API<br>