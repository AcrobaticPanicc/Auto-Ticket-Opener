import requests
import os


class FdeskTools:
    AGENTS_ID = os.environ.get('AGENTS_ID')
    TICKET_FIELDS_URL = os.environ.get('TICKET_FIELDS')

    def __init__(self, api_key):
        self.api_key = api_key

    def get_agent_id(self, agent_name):
        """
        Each Tech Support representative has his own unique ID in Freshdesk.
        Since I am not authorized to reach the endpoint that expose the ID of each representative, I had to find a way
        to get the agent ID.
        :param agent_name: The agent full name exactly as it appear in FreshDesk.
        :return: The given agent ID, or None if agent is not found.
        """
        response = requests.get(self.TICKET_FIELDS_URL, auth=(self.api_key, 'x'))

        for x in response.json():
            if x['id'] == self.AGENTS_ID:
                return x.get('choices').get(agent_name)
