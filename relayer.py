import os
import json
from flask import Flask, request, jsonify
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
from brownie import accounts, network
from scripts.config_manager import get_network_config, get_contract_address


load_dotenv()

"""
This script sets up a Flask server to handle signing and relaying Ethereum transactions.
It uses the web3.py library to interact with the Ethereum blockchain and the Brownie framework for contract interaction.
"""

MIXER_CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS_MAINNET")
network_name, provider_url = get_network_config()
network.connect(network_name)
w3 = Web3(HTTPProvider(provider_url))

with open("build/contracts/EthereumMixer.json", "r") as file:
    MIXER_CONTRACT_ABI = json.load(file)['abi']



contract = w3.eth.contract(address=MIXER_CONTRACT_ADDRESS, abi=MIXER_CONTRACT_ABI)

print(f'Network: {network.show_active()}')
print(f'Contract address: {contract.address}')

app = Flask(__name__)

def log_to_dict(log):
    return {
        'address': log.address,
        'topics': [topic.hex() for topic in log.topics],
        'data': log.data,  # Remove .hex() here
        'blockHash': log.blockHash.hex(),
        'blockNumber': log.blockNumber,
        'transactionHash': log.transactionHash.hex(),
        'transactionIndex': log.transactionIndex,
        'blockNumber': log.blockNumber,
        'logIndex': log.logIndex,
        'removed': log.removed
    }


def receipt_to_dict(receipt):
    return {
        'transactionHash': receipt.transactionHash.hex(),
        'transactionIndex': str(receipt.transactionIndex),
        'blockHash': receipt.blockHash.hex(),
        'blockNumber': str(receipt.blockNumber),
        'from': receipt['from'],
        'to': receipt.to,
        'gasUsed': str(receipt.gasUsed),
        'cumulativeGasUsed': str(receipt.cumulativeGasUsed),
        'contractAddress': receipt.contractAddress,
        'logs': [log_to_dict(log) for log in receipt.logs],
        'status': str(receipt.status),
        'logsBloom': receipt.logsBloom.hex()
    }

@app.route('/sign', methods=['POST'])
def sign():
    data = request.json
    _to = data['_to']
    _amount = int(data['_amount'])
    signer_private_key = data.get('signer_private_key')
    if not signer_private_key:
        raise ValueError("Signer private key not found")

    message = Web3.solidityKeccak(['address', 'uint256', 'address'], [_to, _amount, MIXER_CONTRACT_ADDRESS])
    signable_message = encode_defunct(hexstr=message.hex())
    signature = w3.eth.account.sign_message(signable_message, private_key=signer_private_key)
    return jsonify({
        'signature': signature.signature.hex()
    })

@app.route('/relay', methods=['POST'])
def relay():
    data = request.json
    _to = data['_to']
    _amount = int(data['_amount'])
    _signature = data['_signature']

    if not _signature:
        raise ValueError("Signature not provided")

    relayer_private_key = os.getenv("PRIVATE_KEY_4")
    relay_account = accounts.add(relayer_private_key)

    balance = w3.eth.get_balance(relay_account.address)
    if balance < (200000 * w3.eth.gas_price):  # Assuming gas price is fetched from the network
        raise ValueError("Insufficient funds for transaction")

    tx = contract.functions.withdraw(_to, _amount, _signature).buildTransaction({
        'gas': 100000,
        'nonce': w3.eth.getTransactionCount(relay_account.address)
    })

    signed_tx = w3.eth.account.signTransaction(tx, private_key=relayer_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction).hex()

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    receipt_dict = receipt_to_dict(receipt)

    if receipt.status == 0:
        return jsonify({'error': 'Transaction failed', 'receipt': receipt_dict}), 400
    
    return jsonify({
        'transaction_hash': tx_hash,
        'receipt': receipt_dict
    })

if __name__ == '__main__':
    app.run(debug=True)
