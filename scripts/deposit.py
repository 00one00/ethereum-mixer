from brownie import accounts, EthereumMixer
from web3 import Web3
from dotenv import load_dotenv
from .config_manager import load_account, fetch_env_variable


load_dotenv()

def deposit(amount_ether, index=0):
    mixer = EthereumMixer[-1]

    account = load_account(index)

    print(f'Depositer account: {account.address}')

    amount_wei = Web3.toWei(amount_ether, "ether")

    tx = mixer.deposit({"from": account, "value": amount_wei})
    tx.wait(1)

    print(f"Deposited {amount_ether} Ether (or {amount_wei} wei) to the contract.")
    print(f"Transaction hash: {tx.txid}")
    

def main():
    amount = fetch_env_variable("DEPOSIT_AMOUNT", default="0.02", required=False)
    index = fetch_env_variable("DEPOSIT_INDEX", default="12", required=False)
    deposit(float(amount), int(index))