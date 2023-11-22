from .config_manager import load_account
from brownie import EthereumMixer

def execute_emergency_withdraw():
    owner = load_account()
    contract = EthereumMixer[-1]
    tx = contract.emergencyWithdraw({"from": owner})
    tx.wait(1)
    print(f"Emergency withdrawal executed. Transaction hash: {tx.id}")

def main():
    execute_emergency_withdraw()