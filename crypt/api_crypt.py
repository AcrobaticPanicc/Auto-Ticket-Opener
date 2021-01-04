import keyring
from cryptography.fernet import Fernet
from keyring.backends import Windows


class Crypt:
    """
    This class is used to encrypt and decrypt the Freshdesk API key.
    """

    def __init__(self):
        keyring.set_keyring(Windows.WinVaultKeyring())

    def encrypt_api_key(self, api_key):
        """
        Encrypts the API Key using the encription key
        :param api_key:
        :return:
        """
        api_key = api_key.encode()
        f = Fernet(self._load_key())
        encrypted_api_key = f.encrypt(api_key)
        return encrypted_api_key.decode('utf-8')

    def decrypt_api_key(self, encrypted_api_key):
        """
        Decrypt the API key
        :param encrypted_api_key: 
        :return: decrypted_api_key
        """
        key = self._load_key()
        f = Fernet(key)
        decrypted_api_key = f.decrypt(encrypted_api_key.encode())
        return decrypted_api_key.decode()

    @staticmethod
    def _load_key():
        """
        Reuturn the encription key from Windows Credential
        :return: encription key
        """
        return keyring.get_password('cryptography', 'key')

    @staticmethod
    def generate_key():
        """
        Generates a random key that will be used
        to encrypt and decrypt the API key
        """
        key = Fernet.generate_key()
        keyring.set_password('cryptography', 'key', key.decode('utf-8'))
