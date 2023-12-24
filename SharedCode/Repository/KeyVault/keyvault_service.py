from .keyvault_factory import KeyVaultFactory
import json

class KeyVaultService:
    def __init__(self):
        self.client = KeyVaultFactory.get_client()

    def get_secret(self, secret_name):
        return self.client.get_secret(secret_name).value

    def set_secret(self, secret_name, secret_value):
        return self.client.set_secret(secret_name, secret_value).value
    
    def get_fyers_user(self, index:int):
        fyer_users_json = self.get_secret("FyerUserDetails")
        fyer_users = json.loads(fyer_users_json)
        fyers_details_json = self.get_secret(fyer_users[index]["KvSecretName"])
        fyers_details = json.loads(fyers_details_json)
        return fyers_details
