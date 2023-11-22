import requests
from web3 import Web3
import os
from dotenv import load_dotenv
from .config_manager import get_private_key_by_index

load_dotenv()

RELAYER_ENDPOINT = "http://127.0.0.1:5000"
def sign_withdraw(receiver, amount_ether, signer_private_key):
    _amount = Web3.toWei(amount_ether, "ether")

    print(f"Signing for {_amount} wei to send to {receiver}")

    response = requests.post(f"{RELAYER_ENDPOINT}/sign", json={
        "_to": receiver,
        "_amount": _amount,
        'signer_private_key': signer_private_key
    })

    if response.status_code == 200:
        signature = response.json()['signature']
        print("Successfully signed the message.")
        print("Signature:", signature)
        return signature 
    else:
        print("Error:", response.text)
        return None

def main():
   receiver_accounts = [os.getenv("RECEIVER_ACCOUNT_1"), os.getenv("RECEIVER_ACCOUNT_2"), os.getenv("RECEIVER_ACCOUNT_3"), 
                        os.getenv("RECEIVER_ACCOUNT_4"), os.getenv("RECEIVER_ACCOUNT_5"), os.getenv("RECEIVER_ACCOUNT_6"), os.getenv("RECEIVER_ACCOUNT_7")]
   receiver_amount = float(os.getenv("DEPOSIT_AMOUNT_1")) / 7
   signer_key = os.getenv("PRIVATE_KEY_12")
   for account in receiver_accounts:
       sign_withdraw(account, receiver_amount, signer_key)
    