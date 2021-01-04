import keyring
from crypt.api_crypt import Crypt
from keyring.backends import Windows


def get_info():
    """
    :return: The saved information from Windows Credential
    """
    keyring.set_keyring(Windows.WinVaultKeyring())

    return dict(
        api_key=Crypt().decrypt_api_key(keyring.get_password('freshdesk', 'api_key')),
        agent_id=keyring.get_password('freshdesk', 'agnet_id'),
        internal_username=keyring.get_password('internal', 'username'),
        internal_cookies=keyring.get_password('internal', 'cookies'),
        agent_name=keyring.get_password('freshdesk', 'agent_name'),
        full_name=keyring.get_password('freshdesk', 'full_agent_name')
    )
