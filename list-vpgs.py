import requests
import json
import warnings
import os
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # Correct import statement

# Suppress only the InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

# Configuration variables
ZVM_ADDRESS = os.getenv("ZVM_ADDRESS", "172.16.50.100")
ZVM_USERNAME = os.getenv("ZVM_USERNAME", "admin")
ZVM_PASSWORD = os.getenv("ZVM_PASSWORD", "Zertodata987!")
VERIFY_CERTIFICATE = os.getenv("VERIFY_CERTIFICATE", "False").lower() in ('true', '1', 't')

# Nothing below should need modified for the example to run and list VPGs

KEYCLOAK_API_BASE = f"https://{ZVM_ADDRESS}/auth/realms/zerto/protocol/openid-connect/token"
ZVM_API_BASE = f"https://{ZVM_ADDRESS}/v1/"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#function to get a token from keycloak
def get_token():
    uri = KEYCLOAK_API_BASE
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'username': ZVM_USERNAME,
        'password': ZVM_PASSWORD,
        'grant_type': 'password',
        'client_id': 'zerto-client'  # This is typically required for the password grant
    }

    try:
        response = requests.post(uri, headers=headers, data=body, verify=VERIFY_CERTIFICATE)
        response.raise_for_status()
        token_data = response.json()
        logging.info(f"Got Token Data: {token_data}")
        return token_data.get('access_token')
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        logging.error(f"Error obtaining token: {e}")
        return None

# main function which executes when the program is run
def run():

    # authenticate to the zvm
    token = get_token()
    if not token:
        logging.error("Failed to get token.")
        return

    # this line can be adjusted to any API url in ZVM
    uri = f"{ZVM_API_BASE}vpgs"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    body = {}

    try:
        # this line will need to be modified depending on if the api you want is a GET, POST, PUT, DELETE, etc
        response = requests.get(uri, headers=headers, json=body, verify=VERIFY_CERTIFICATE),
        response.raise_for_status()
        logging.info(f'Request successful.\n{response.json()}')
        return
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Zerto API failed: {e}")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return

if __name__ == '__main__':
    run()
