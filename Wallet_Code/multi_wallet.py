## Imports
import subprocess
import json
from constraints import *
import os
from dotenv import load_dotenv

from web3 import Web3
from bit import *
from eth_account import Account

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Add POA Middleware
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# Read in the mnemonic, saved as an environment variable
load_dotenv()
mnemonic = os.getenv('MNEMONIC')

# Derive function
def derive_wallets(coin):
    command = './derive -g --mnemonic="'+str(mnemonic)+'" --cols=path,address,privkey,pubkey --numderive=5 --coin='+str(coin)+' --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

# Using the derive function, create an object to store the output for ETH and BTCTEST
coins = {ETH: derive_wallets(ETH),BTCTEST:derive_wallets(BTCTEST)}

## Select the private keys, respectively, for each coin
eth_private_key = coins['eth'][0]['privkey']
btc_private_key = coins['btc-test'][0]['privkey']

# Functions

## This will convert the `privkey` string in a child key to an account object
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

## This will create the raw, unsigned transaction that contains all metadata needed to transact.

def create_tx (coin, account, to, amount):
    if coin == ETH:
        value = w3.toWei(amount, "ether")
        gasEstimate = w3.eth.estimateGas({ "to": to, "from": account.address, "amount": value})
        return {
            "to": to,
            "from": account.address,
            "amount": value,
            "gas": gasEstimate,
           "gasPrice": w3.eth.generateGasPrice(),
            "nonce": w3.eth.getTransactionCount(account.address),
           "chainId": w3.net.chainId
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

## This will call `create_tx`, sign the transaction, then send it to the designated network.
def send_tx(coin, account, to, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(raw_tx)
        return w3.eth.sendRawTransaction(signed.sendRawTransaction)
    
    elif coin == BTCTEST:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.sign_transaction(raw_tx)
        from bit.network import NetworkAPI
        return NetworkAPI.broadcast_tx_testnet(signed)
        

# Send Transaction for BTC

## Fund the first address
funding_address = coins['btc-test'][0]['address']

## Set up the from account and the to address
btc_address_from = coins[BTCTEST][0]['privkey']
btc_address_to = coins[BTCTEST][1]['address']

## Initialize the send_tx
from bit import wif_to_key
key_1 = wif_to_key(btc_address_from)
key_2 = wif_to_key(coins[BTCTEST][1]['privkey'])

print(f'From Address Balance:{key_1.get_balance("btc")}')
print(f'To Address Balance:{key_2.get_balance("btc")}')

#send_tx(BTCTEST, priv_key_to_account(BTCTEST, btc_address_from), btc_address_to, 0.0000001)

# Send Transaction for ETH

ethereum_network_address = coins['eth'][0]['address']
print(ethereum_network_address)

#