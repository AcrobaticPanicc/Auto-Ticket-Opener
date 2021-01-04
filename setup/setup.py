import json
import requests
from bs4 import BeautifulSoup
from crypt.api_crypt import Crypt
from freshdesk.fdesk_tools import FdeskTools
import keyring
from keyring.backends import Windows
import os


class Setup:
    HEADERS = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    }
    TICKET_FIELDS_URL = os.environ.get('TICKET_FIELDS_URL')
    INTERNAL_URL = os.environ.get('INTERNAL_URL')

    def __init__(self):
        keyring.set_keyring(Windows.WinVaultKeyring())
        self.crypt = Crypt()
        self.crypt.generate_key()

    def setup_freshdesk(self, agent_name: str, api_key: str):
        """
        Saving relavent Freshdesk info in Windows Credential.
        :param agent_name: Freshdesk agent full name. EXAMPLE: Johnny Cage.
        :param api_key: The Freshdesk API Key.
        """
        agent_name = agent_name.strip().title()
        api_key = api_key.strip()

        response = requests.get(self.TICKET_FIELDS_URL, auth=(api_key, 'x'))

        if response.status_code == 200:
            try:
                agent_id = FdeskTools(api_key).get_agent_id(agent_name)

                if agent_id:
                    encrypted_api_key = self.crypt.encrypt_api_key(api_key)
                    keyring.set_password("freshdesk", "api_key", encrypted_api_key)
                    keyring.set_password("freshdesk", "agnet_id", f"{agent_id}")
                    keyring.set_password("freshdesk", "agent_name", agent_name.replace(' ', '')),
                    keyring.set_password("freshdesk", "full_agent_name", agent_name)
                    return True

            except KeyError:
                print('Username was not found')
                return False

        return None

    def setup_internal(self, internal_username):
        internal_username = internal_username.strip()
        session = requests.Session()

        internal_login_url = self.INTERNAL_URL
        login_data = {
            'UserName': internal_username,
            'Password': internal_username * 2,
            'LoginButton': 'Log In'
        }

        response = session.get(internal_login_url, headers=self.HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        login_data['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']

        # login to internal
        response = session.post(internal_login_url, data=login_data, headers=self.HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')

        # check if successfully logged in
        if soup.find('title').text == 'Staff Login':
            return None

        # save cookies and internal user
        cookies_dict = dict(session.cookies)
        username = cookies_dict['Login'].split('=')[1]
        keyring.set_password("internal", "username", username)
        keyring.set_password("internal", "cookies", json.dumps(cookies_dict))
        return True

    def refresh_internal_cookies(self):
        internal_username = keyring.get_password("internal", "username")
        self.setup_internal(internal_username)
