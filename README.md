# Ethereum Mixer
## Project Overview

Ethereum Mixer is a smart contract system designed to enhance privacy in Ethereum transactions. It enables users to deposit Ethereum (ETH) and withdraw it to different addresses, increasing anonymity. The system includes a mixer contract on the Ethereum network and Python scripts for contract interaction.

## Prerequisites
* Node.js
* Python (3.7+)
* Brownie
* Solidity

## Environment Setup
### Brownie Configuration
Create a brownie-config.yaml file in your project's root directory with the following network configurations and wallets:
```
networks:
  default:
    mainnet
  ganache:
    host: HTTP://127.0.0.1:7545
    chainid: 5777
  development:
    host: http://127.0.0.1:8545
  goerli:
    host: https://goerli.infura.io/v3/${WEB3_INFURA_PROJECT_ID}
    accounts:
      - id: account1
        cmd: brownie accounts new account1
      - id: account2
        cmd: brownie accounts new account2
  sepolia:
    host: https://sepolia.infura.io/v3/${WEB3_INFURA_PROJECT_ID}
    chainid: 11155111
  mainnet:
    host: https://mainnet.infura.io/v3/${WEB3_INFURA_PROJECT_ID}

wallets:
  from_key_1: ${PRIVATE_KEY_1}
  ...
  from_key_13: ${PRIVATE_KEY_13}
  from_mnemonic_1: ${MNEMONIC_1}
  from_mnemonic_2: ${MNEMONIC_2}

dotenv: .env
```

Environment Variables
Create a `.env` file with the necessary variables:
```
PRIVATE_KEY_1=your_private_key_here
...
PRIVATE_KEY_13=your_private_key_here
MNEMONIC_1=your_mnemonic_here
MNEMONIC_2=your_mnemonic_here
WEB3_INFURA_PROJECT_ID=your_infura_project_id_here
```

Installation
1. Clone the repository:
`git clone https://github.com/00one00/ethereum-mixer.git`
2. Install dependencies:
```
npm install
pip install -r requirements.txt
```

## Deployment Guide
To deploy the Ethereum Mixer contract:

1. Test on Sepolia Testnet:
`brownie run deploy.py --network sepolia`
2. Deploy to Ethereum Mainnet:
`brownie run deploy.py --network mainnet`

## Script Usage
`deploy.py`: Deploys the EthereumMixer contract.


`deposit.py`: Enables ETH deposits into the mixer.
+ Usage: brownie run deposit.py --network [network]


`sign_withdraw.py`: Signs withdrawal transactions.
+ Usage: brownie run sign_withdraw.py --network [network]


`relay_withdraw.py`: Relays a signed withdrawal transaction.
+ Usage: brownie run relay_withdraw.py --network [network]


### Relayer Setup
`relayer.py`: A Flask server that handles transaction signing and relaying.
Run in a separate terminal environment: `python relayer.py`.

## How It Works
The Ethereum Mixer enhances transaction privacy on the Ethereum blockchain through:

### Smart Contract (EthereumMixer.sol):

1. Deposit: Users deposit ETH. The contract records the amount against the depositor's address.
2. Withdrawal: Users withdraw ETH to a different address using a signed message, enhancing privacy.
Python Scripts:

Facilitate contract interaction, including depositing ETH and signing/relaying withdrawals.
### Relayer (Flask Server):

Handles signing and relaying transactions, obscuring the link between deposit and withdrawal transactions.

## FAQ
Q: What is the main purpose of Ethereum Mixer?
A: To increase privacy and anonymity in Ethereum transactions by allowing users to deposit and withdraw ETH without direct linkage between the two actions.

Q: Is it necessary to run relayer.py for the system to work?
A: Yes, relayer.py is essential as it handles the signing and relaying of withdrawal transactions.

Q: How do I obtain a signature for a withdrawal?
A: Use sign_withdraw.py to generate a signature. The script requires the receiver's address, withdrawal amount, and signer's private key.

Q: Can I test the system before deploying it to the Ethereum mainnet?
A: Yes, testing on networks like Sepolia or Goerli is recommended before mainnet deployment.

Q: What security measures should I take when using Ethereum Mixer?
A: Keep private keys secure, avoid hardcoding sensitive information, and regularly update dependencies.

Q: Where can I seek help if I encounter issues?
A: For issues, questions, or contributions, please create an issue on the GitHub repository.

Stay Connected

X: @nonfungible_kid


Donate Ethereum (Mainnet): 0xF3aB84bddFD1536d421DCA2f1eB7198C5cBB6990
>>>>>>> 57d5511 (Initial commit)
