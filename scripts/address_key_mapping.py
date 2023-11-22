import os
from .config_manager import load_account, get_private_key
import json

"""
This script generates a mapping of Ethereum addresses to their corresponding private keys.
It saves the mapping to a JSON file for later use.
"""

def main():
    """
    The main function to be executed for the script.
    It iterates through a specified number of accounts, retrieves their addresses and private keys,
    and saves them to a JSON file.
    """
    account_number = 0
    number_of_accounts = 13 # number of accounts you wish to add to key dictionary
    accounts_list = [load_account(i) for i in range(number_of_accounts)] 
    keys_config = {}

    for account in accounts_list:
        account_number += 1
        print(f"Account{account_number} address: {account.address}")
        # Assuming the private keys are stored in environment variables named PRIVATE_KEY_1, PRIVATE_KEY_2, etc.
        env_var_name = f"PRIVATE_KEY_{account_number}"
        private_key = get_private_key(env_var_name)
        keys_config[account.address] = private_key

    # Save the keys_config dictionary to a json file
    with open("keys_config.json", "w") as file:
        json.dump(keys_config, file, indent=4)

    print(f"Keys configuration saved to keys_config.json")
