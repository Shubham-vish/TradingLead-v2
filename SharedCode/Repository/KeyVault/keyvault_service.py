from .keyvault_factory import KeyVaultFactory


class KeyVaultService:
    def __init__(self):
        self.client = KeyVaultFactory.get_client()

    def get_secret(self, secret_name):
        return self.client.get_secret(secret_name).value

    def set_secret(self, secret_name, secret_value):
        return self.client.set_secret(secret_name, secret_value).value
