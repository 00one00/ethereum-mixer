import requests
from web3 import Web3
import os
from dotenv import load_dotenv
from .sign_withdraw import sign_withdraw

load_dotenv()

def relay_withdraw(_to, amount_ether, _signature=None):
    RELAYER_ENDPOINT = "http://127.0.0.1:5000"
    _amount = Web3.toWei(amount_ether, "ether")

    if _signature is None:
        _signature = sign_withdraw(_to, amount_ether)

    print(f"Relaying withdraw to {_to} for {_amount} wei using signature {_signature}")

    response = requests.post(f"{RELAYER_ENDPOINT}/relay", json={
        "_to": _to,
        "_amount": _amount,
        "_signature": _signature
    })

    if response.status_code == 200:
        print("Successfully relayed the transaction.")
        print("Transaction hash:", response.json()['transaction_hash'])
    else:
        print("Error:", response.text)

def main():
    receiver_account1 = os.getenv('RELAYER_ACCOUNT')
    receiver_account2 = os.getenv('RECEIVER_ACCOUNT_2')
    split_relay_amount = float(os.getenv("RELAY_AMOUNT_ETH")) / 2
    full_relay_amount = float(os.getenv("RELAY_AMOUNT_ETH"))
    depositor_1_amount = os.getenv("DEPOSIT_AMOUNT_1")
    depositor_2_amount = os.getenv("DEPOSIT_AMOUNT_2")
    signature = os.getenv("SIGNATURE")
    signatures_str = os.getenv("SIGNATURES")
    if signatures_str is None:
        raise EnvironmentError("SIGNATURES environment variable not found.")
    signatures_list = signatures_str.split(',')

    # Now you can access individual signatures by index
    signature1 = signatures_list[0]
    signature2 = signatures_list[1]


    receiver_accounts = [os.getenv("RECEIVER_ACCOUNT_1"), os.getenv("RECEIVER_ACCOUNT_2"), os.getenv("RECEIVER_ACCOUNT_3"), 
                        os.getenv("RECEIVER_ACCOUNT_4"), os.getenv("RECEIVER_ACCOUNT_5"), os.getenv("RECEIVER_ACCOUNT_6"), os.getenv("RECEIVER_ACCOUNT_7")]
    receiver_amount = float(os.getenv("DEPOSIT_AMOUNT_1")) / 7
    index = 0
    for account in receiver_accounts:
        relay_withdraw(account, receiver_amount, signatures_list[index])
        index += 1