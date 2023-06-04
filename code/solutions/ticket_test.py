sample_data = [
    {
        'display': 'IoT (300)',
        'id': 4,
        'name': 'IoT',
        'url': '/api/ipam/vlans/4/',
        'vid': 300
    },
    {
        'display': 'Data (400)',
        'id': 5,
        'name': 'Data',
        'url': '/api/ipam/vlans/5/',
        'vid': 400
    },
    {
        'display': 'Guests (500)',
        'id': 6,
        'name': 'Guests',
        'url': '/api/ipam/vlans/6/',
        'vid': 500
    }
]

vlan_list = [tag['vid'] for tag in sample_data]
print(vlan_list)

# # from pprint import pprint
# #
# # map = {
# #     "ticket_number": "Change ticket",
# #     "device_name": "Device",
# #     "interface_name": "Interface",
# #     "interface_enabled": "Interface enabled?",
# #     "interface_description": "Interface description",
# #     "interface_mtu": "Interface MTU",
# #     "interface_mode": "Interface mode",
# #     "untagged_vlan": "Untagged/native VLAN ID",
# #     "tagged_vlans": "Allowed VLAN tags",
# #     "interface_ipv4": "IPv4 address"
# # }
# #
# # sample_data = {'ticket_number': '15002',
# #                'device_name': 'c9300',
# #                'interface_name': 'GigabitEthernet1/0/1',
# #                'interface_enabled': False,
# #                'interface_mtu': 1500,
# #                'interface_description': 'aasdf',
# #                'interface_mode': 'access',
# #                'untagged_vlan': 200,
# #                'tagged_vlans': [],
# #                'interface_ipv4': None}
# #
# # out_list = []
# # output = {}
# # for k, v in sample_data.items():
# #     out_list.append({"title": map[k],
# #                      "value": v})
# #
# # pprint(out_list, indent=4)
# #
#
# import os
# from zammad_py import ZammadAPI
# import pprint
#
#
# ticket_client = ZammadAPI(url=os.environ.get("TICKET_URL"),
#                           username=os.environ.get("TICKET_USERNAME"),
#                           password=os.environ.get("TICKET_PASSWORD"))
#
# # ticket = ticket_client.ticket.find(7)
# ticket = ticket_client.ticket.search({"query": "number:15003"})
# pprint.pprint(ticket, indent=4)
# #
# # # print(dir(ticket_client.ticket_state))
# # states = ticket_client.ticket_state.all()
# # # pprint.pprint(states, indent=4)
# # for state in states:
# #     pprint.pprint(state, indent=4)
# #     if state['name'] == "pending approval":
# #         next_state = state['id']
# #         break
# # print(f"Next state: {next_state}")
# # params = {
# #     "state": "pending approval",
# #     "article": {
# #         "body": "Another update.",
# #         "type": "note",
# #         "internal": False
# #     }
# # }
# # #
# # #
# # #
# # new_ticket = ticket_client.ticket.update(id=7, params=params)
# #
# # #
# # # NOTE - Default ticket overviews AFTER running the rails script to update new states:
# # [
# #     {
# #         "id": 1,
# #         "name": "My Assigned Tickets",
# #         "link": "my_assigned",
# #         "prio": 1000,
# #         "condition": {
# #             "ticket.state_id": {
# #                 "operator": "is",
# #                 "value": [
# #                     2,
# #                     1,
# #                     3,
# #                     7
# #                 ]
# #             },
# #             "ticket.owner_id": {
# #                 "operator": "is",
# #                 "pre_condition": "current_user.id"
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "ASC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "s": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": true,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:30.972Z",
# #         "updated_at": "2023-05-27T16:25:53.677Z",
# #         "role_ids": [
# #             2
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 2,
# #         "name": "Unassigned & Open Tickets",
# #         "link": "all_unassigned",
# #         "prio": 1010,
# #         "condition": {
# #             "ticket.state_id": {
# #                 "operator": "is",
# #                 "value": [
# #                     2,
# #                     1,
# #                     3
# #                 ]
# #             },
# #             "ticket.owner_id": {
# #                 "operator": "is",
# #                 "pre_condition": "not_set"
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "ASC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "s": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": false,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.020Z",
# #         "updated_at": "2023-05-27T16:25:56.543Z",
# #         "role_ids": [
# #             2
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 3,
# #         "name": "My Pending Reached Tickets",
# #         "link": "my_pending_reached",
# #         "prio": 1020,
# #         "condition": {
# #             "ticket.state_id": {
# #                 "operator": "is",
# #                 "value": [
# #                     3
# #                 ]
# #             },
# #             "ticket.owner_id": {
# #                 "operator": "is",
# #                 "pre_condition": "current_user.id"
# #             },
# #             "ticket.pending_time": {
# #                 "operator": "before (relative)",
# #                 "value": 0,
# #                 "range": "minute"
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "ASC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "s": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": false,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.028Z",
# #         "updated_at": "2023-05-27T16:25:59.390Z",
# #         "role_ids": [
# #             2
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 4,
# #         "name": "My Subscribed Tickets",
# #         "link": "my_subscribed_tickets",
# #         "prio": 1025,
# #         "condition": {
# #             "ticket.mention_user_ids": {
# #                 "operator": "is",
# #                 "pre_condition": "current_user.id",
# #                 "value": "",
# #                 "value_completion": ""
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "ASC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "s": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "created_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": false,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.035Z",
# #         "updated_at": "2023-05-27T16:26:02.263Z",
# #         "role_ids": [
# #             2
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 5,
# #         "name": "Open Tickets",
# #         "link": "all_open",
# #         "prio": 1030,
# #         "condition": {
# #             "ticket.state_id": {
# #                 "operator": "is",
# #                 "value": [
# #                     2,
# #                     1,
# #                     3
# #                 ]
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "ASC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "state",
# #                 "owner",
# #                 "created_at"
# #             ],
# #             "s": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "state",
# #                 "owner",
# #                 "created_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "state",
# #                 "owner",
# #                 "created_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": true,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.042Z",
# #         "updated_at": "2023-05-27T16:26:05.131Z",
# #         "role_ids": [
# #             2
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 6,
# #         "name": "Pending Reached Tickets",
# #         "link": "all_pending_reached",
# #         "prio": 1040,
# #         "condition": {
# #             "ticket.state_id": {
# #                 "operator": "is",
# #                 "value": [
# #                     3
# #                 ]
# #             },
# #             "ticket.pending_time": {
# #                 "operator": "before (relative)",
# #                 "value": 0,
# #                 "range": "minute"
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "ASC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "created_at"
# #             ],
# #             "s": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "created_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "created_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": false,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.050Z",
# #         "updated_at": "2023-05-27T16:26:08.043Z",
# #         "role_ids": [
# #             2
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 7,
# #         "name": "Escalated Tickets",
# #         "link": "all_escalated",
# #         "prio": 1050,
# #         "condition": {
# #             "ticket.escalation_at": {
# #                 "operator": "till (relative)",
# #                 "value": "10",
# #                 "range": "minute"
# #             }
# #         },
# #         "order": {
# #             "by": "escalation_at",
# #             "direction": "ASC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "escalation_at"
# #             ],
# #             "s": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "escalation_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "escalation_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": false,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.057Z",
# #         "updated_at": "2023-05-27T16:26:12.112Z",
# #         "role_ids": [
# #             2
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 8,
# #         "name": "My Replacement Tickets",
# #         "link": "my_replacement_tickets",
# #         "prio": 1080,
# #         "condition": {
# #             "ticket.state_id": {
# #                 "operator": "is",
# #                 "value": [
# #                     2,
# #                     1,
# #                     3,
# #                     7
# #                 ]
# #             },
# #             "ticket.out_of_office_replacement_id": {
# #                 "operator": "is",
# #                 "pre_condition": "current_user.id"
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "DESC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": true,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "escalation_at"
# #             ],
# #             "s": [
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "escalation_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "group",
# #                 "owner",
# #                 "escalation_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": false,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.064Z",
# #         "updated_at": "2023-05-27T16:26:14.964Z",
# #         "role_ids": [
# #             2
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 9,
# #         "name": "My Tickets",
# #         "link": "my_tickets",
# #         "prio": 1100,
# #         "condition": {
# #             "ticket.state_id": {
# #                 "operator": "is",
# #                 "value": [
# #                     2,
# #                     1,
# #                     3,
# #                     4,
# #                     6,
# #                     7
# #                 ]
# #             },
# #             "ticket.customer_id": {
# #                 "operator": "is",
# #                 "pre_condition": "current_user.id"
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "DESC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": false,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "state",
# #                 "created_at"
# #             ],
# #             "s": [
# #                 "number",
# #                 "title",
# #                 "state",
# #                 "created_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "state",
# #                 "created_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": true,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.073Z",
# #         "updated_at": "2023-05-27T16:26:17.838Z",
# #         "role_ids": [
# #             3
# #         ],
# #         "user_ids": []
# #     },
# #     {
# #         "id": 10,
# #         "name": "My Organization Tickets",
# #         "link": "my_organization_tickets",
# #         "prio": 1200,
# #         "condition": {
# #             "ticket.state_id": {
# #                 "operator": "is",
# #                 "value": [
# #                     2,
# #                     1,
# #                     3,
# #                     4,
# #                     6,
# #                     7
# #                 ]
# #             },
# #             "ticket.organization_id": {
# #                 "operator": "is",
# #                 "pre_condition": "current_user.organization_id"
# #             }
# #         },
# #         "order": {
# #             "by": "created_at",
# #             "direction": "DESC"
# #         },
# #         "group_by": null,
# #         "group_direction": null,
# #         "organization_shared": true,
# #         "out_of_office": false,
# #         "view": {
# #             "d": [
# #                 "title",
# #                 "customer",
# #                 "organization",
# #                 "state",
# #                 "created_at"
# #             ],
# #             "s": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "organization",
# #                 "state",
# #                 "created_at"
# #             ],
# #             "m": [
# #                 "number",
# #                 "title",
# #                 "customer",
# #                 "organization",
# #                 "state",
# #                 "created_at"
# #             ],
# #             "view_mode_default": "s"
# #         },
# #         "active": false,
# #         "updated_by_id": 3,
# #         "created_by_id": 1,
# #         "created_at": "2023-05-27T16:22:31.080Z",
# #         "updated_at": "2023-05-27T16:26:22.100Z",
# #         "role_ids": [
# #             3
# #         ],
# #         "user_ids": []
# #     }
# # ]