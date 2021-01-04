import json
import keyring
import requests
from bs4 import BeautifulSoup
from setup.setup import Setup
import os


class Internal:
    INTERNAL_SEARCH_URL = os.environ.get('INTERNAL_SEARCH_URL')
    INTERNAL_URL = os.environ.get('INTERNAL_URL')

    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        }
        self.session = requests.Session()

    def _check_if_logged_in(self):
        """
        Check if the user is connected to the current session.
        If is is not, it is refreshing the internal cookies and logging the user in.
        :return: True if successfully connected
        """
        self._add_cookies()
        soup = self._get_soup()

        if soup.find('title').text.strip() != '':
            Setup().refresh_internal_cookies()
            self._check_if_logged_in()

        return True

    def _add_cookies(self):
        # adding cookies to the session
        cookies_dict = json.loads(keyring.get_password("internal", "cookies"))
        self.session.cookies.update(cookies_dict)

    def _get_soup(self):
        # return the soup object of the current session
        response = self.session.get(self.INTERNAL_SEARCH_URL, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def search_user(self, username):
        self._add_cookies()
        soup = self._get_soup()

        if soup.find('title').text.strip() != '':
            self._check_if_logged_in()
            soup = self._get_soup()

        search_by = ['LoginName', 'Email']
        for by in search_by:
            search_query = {
                'ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DropClientSearch': by,
                'ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$TxtSearchtext': username,
                'ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$BtnClientSearch': 'Search',
                '__VIEWSTATE': soup.find('input', attrs={'id': '__VIEWSTATE'})['value'],
                '__VIEWSTATEGENERATOR': soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'})['value']}

            query = self.session.post(self.INTERNAL_SEARCH_URL, data=search_query, headers=self.headers)
            response_content = BeautifulSoup(query.text, 'html.parser')

            res_table_row = response_content.find('tr', {'class': 'ClientProductVersion__MainRow_Header_Gray'})

            if res_table_row:
                res_table_cols = res_table_row.findAll('td')
                return {
                    'user_login': res_table_cols[1].text,
                    'user_email': res_table_cols[4].text,
                    'user_id': res_table_cols[9].text
                }

        return None

    def check_vpn_connection(self):
        """
        Access to Internal is possible only with a VPN connection.
        This function check if Internal is accessible.
        :return: True if VPN is connected, False else.
        """
        try:
            requests.get(self.INTERNAL_URL)
            return True

        except requests.exceptions.SSLError:
            return False
