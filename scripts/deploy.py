from brownie import EthereumMixer
from web3 import Web3
from .config_manager import load_account
import logging

logging.basicConfig(level=logging.INFO)


"""
This script handles the deployment of the EthereumMixer smart contract using the Brownie framework.
"""

def deploy(index=0):
    """
    Deploys the EthereumMixer contract to the blockchain.

    Parameters:
    index (int): The index of the account to deploy the contract from.

    Returns:
    None
    """
    deployer = load_account(index)
    
    mixer = EthereumMixer
    try:
        print("Deploying contract...")
        EthereumMixer.deploy({"from": deployer})
        logging.info(f"Contract successfully deployed to {mixer.address}\nContract Owner: {deployer.address}")
    except Exception as e:
        logging.error(f"Deployment failed: {e}")
def main():
    deploy(10)
