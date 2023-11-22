import os
import json
from dotenv import load_dotenv
from brownie import network, accounts, config
from web3 import Web3, HTTPProvider

"""
This script manages the configuration settings for the Ethereum mixer project.
It handles network configurations, account retrieval, and private key management.
"""

def get_contract_address():
    active_network = network.show_active()
    print(f"Active network: {active_network}")
    
    if active_network == "mainnet":
        address = os.getenv('CONTRACT_ADDRESS_MAINNET')
        print(f"Using mainnet address: {address}")
        return address
    elif active_network == "sepolia":
        address = os.getenv('CONTRACT_ADDRESS_SEPOLIA')
        print(f"Using sepolia address: {address}")
        return address
    else:
        print(f'Please deploy contract or configure contract address to the corresponding network {active_network}')
        return

def get_network_config():
    """
    Retrieves the network configuration, including the network name and provider URL.
    
    Returns:
    tuple: A tuple containing the network name and provider URL.
    """
    NETWORK = os.getenv("NETWORK", default="ganache")
    INFURA_PROJECT_ID = os.getenv("WEB3_INFURA_PROJECT_ID", required=True)
    if NETWORK == "ganache":
        return "ganache", 'http://127.0.0.1:7545'
    else:
        return NETWORK, f'https://{NETWORK}.infura.io/v3/{INFURA_PROJECT_ID}'

def get_private_key(env_var):
    private_key = os.getenv(env_var)
    if not private_key.startswith('0x'):
        private_key = '0x' + private_key
    return private_key

def get_account(index=0, key_or_mnemonic='key'):
    network_name = network.show_active()

    if network_name in ["development", "ganache"]:
        try:
            account = accounts[index]
        except IndexError:
            raise IndexError(f"No account found at index {index}. Ensure you have accounts available in your local environment.")
    else:
        if key_or_mnemonic == 'key':
            private_key = os.getenv(f'PRIVATE_KEY_{index + 1}')
            account = accounts.add(private_key)
        elif key_or_mnemonic == 'mnemonic':
            mnemonic = os.getenv(f'MNEMONIC_{index + 1}')
            account = accounts.from_mnemonic(mnemonic)
        else:
            raise ValueError("Invalid option for key_or_mnemonic. Choose 'key' or 'mnemonic'.")
        
    print(f"Account configuration: {account.address}")
    return account

def get_private_key_for_address(address):
    with open("keys_config.json", "r") as file:
        keys_config = json.load(file)
    return keys_config.get(address)

def get_private_key_by_index(index):
    key = os.getenv(f"PRIVATE_KEY_{index + 1}")
    account = accounts.add(key)
    print(f"Fetching key for account address {account.address}...")
    return key


def load_account(index=0):
    if network.show_active() == "ganache":
        account = accounts[index]
    elif network.show_active() in ["goerli", "sepolia", "mainnet"]:
        account = accounts.add(config["wallets"][f"from_key_{index + 1}"])
    return account

def configure_network_and_accounts():
    NETWORK = os.getenv("NETWORK")
    INFURA_PROJECT_ID = os.getenv("WEB3_INFURA_PROJECT_ID")

    if NETWORK == "ganache":
        network.connect("ganache")
        w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
    else: # Assumes Sepolia or another testnet/mainnet
        network.connect(NETWORK)
        w3 = Web3(HTTPProvider(f'https://{NETWORK}.infura.io/v3/{INFURA_PROJECT_ID}'))
    return w3

def fetch_env_variable(var_name, default=None, required=True):
    """
    Fetches an environment variable.

    Parameters:
    var_name (str): The name of the environment variable.
    default (str): The default value to return if the variable is not found. If None, the variable is considered required.
    required (bool): Whether the environment variable is required.

    Returns:
    str: The value of the environment variable or default if not found and not required.
    
    Raises:
    EnvironmentError: If the variable is required but not found.
    """
    value = os.getenv(var_name)
    if value is None and required:
        raise EnvironmentError(f"Environment variable '{var_name}' not found.")
    return value if value is not None else default