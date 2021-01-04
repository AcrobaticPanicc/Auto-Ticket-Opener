import requests
import json


def get_agent_count(agent_name):
    """
    :param agent_name
    :return: The total tickets opened by the provided agent.
    """
    res = requests.get(f'https://api.countapi.xyz/get/{agent_name}/key')
    return json.loads(res.text)['value']


def get_total_count():
    """
    :return: Total tickets opened by the entire team.
    """
    res = requests.get('https://api.countapi.xyz/get/ato/key')
    return json.loads(res.text)['value']
