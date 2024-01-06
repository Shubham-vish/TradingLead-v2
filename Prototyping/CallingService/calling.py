# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../..")))

from Prototyping.setupConfig import setup_config

setup_config()
# Above lines are only for local notebook testing. Not to be used in production.

# Download the helper library from https://www.twilio.com/docs/python/install
# import os
from twilio.rest import Client
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants

# Set environment variables for your credentials
# Read more at http://twil.io/secure

kv_service = KeyVaultService()

account_sid = kv_service.get_secret(Constants.twilio_account_sid)
auth_token = kv_service.get_secret(Constants.twilio_auth_token)
client = Client(account_sid, auth_token)

call = client.calls.create(
  url="http://demo.twilio.com/docs/voice.xml",
  to="+918770947080",
  from_="+12018449779"
)
#   to="+918770947080",

print(call.sid)