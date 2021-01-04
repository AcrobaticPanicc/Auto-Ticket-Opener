import json
import requests
import pyperclip as pyperclip
import re
import os


class OpenTicket:
    MEDIUM_PRIORITY = 2
    SUPPORT_ID = os.getenv('SUPPORT_ID')
    TICKETS_ENDPOINT = os.environ.get('TICKETS_ENDPOINT')
    BASE_FRESHDESK_URL = os.environ.get('BASE_FRESHDESK_URL')

    def __init__(self, info):
        self.api_key = info['api_key']
        self.agent_id = info['agent_id']
        self.headers = {'Content-Type': 'application/json'}

    def open_ticket(self,
                    ticket_title,
                    operating_system,
                    description,
                    user_email,
                    user_id,
                    user_login,
                    tag='',
                    priority=MEDIUM_PRIORITY,
                    host_application=''):
        special_chars_remover = lambda x: re.sub('[#$/&^%{}]]', '', x)

        ticket = {
            'subject': special_chars_remover(ticket_title),
            'description': special_chars_remover(description),
            'email': special_chars_remover(user_email),
            'priority': priority,
            'status': 2,
            'group_id': self.SUPPORT_ID,
            'responder_id': int(self.agent_id),
            'tags': [tag],
            'custom_fields': {
                'operating_system': special_chars_remover(operating_system),
                'userid': int(user_id),
                'login': user_login,
                'host_application': special_chars_remover(host_application)
            }
        }

        r = requests.post(self.TICKETS_ENDPOINT,
                          auth=(self.api_key, 'x'),
                          headers=self.headers,
                          data=json.dumps(ticket))

        ticket_url = f'{self.BASE_FRESHDESK_URL}/a/tickets/{r.json()["id"]}'
        # copy the ticket to clipboard
        pyperclip.copy(ticket_url)
        return True
