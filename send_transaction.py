from web3 import Web3
from web3.auto import w3
import requests
from eth_account import Account

'''
ganache-cli --fork https://eth-mainnet.g.alchemy.com/v2/5K4nnjROFZ-KzwP-zW-kjclHNYN8E0sp -- unlock 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
'''


def send_transaction(web3_obj, from_address, to_address, amount):
    return web3_obj.eth.send_transaction({
        "from": from_address,
        "to": to_address,
        "value": amount
    })


if __name__ == '__main__':
    whale_acc = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    node_fake = "http://127.0.0.1:8545"

    eth_fake = Web3(Web3.HTTPProvider(node_fake))
    print(len(eth_fake.eth._accounts()))
    print(eth_fake.is_connected())
    print(eth_fake.eth.get_balance(whale_acc))
    print(send_transaction(eth_fake,
          '0xea34C24f3F8f15C0FaCc04f26E7D8870672Cd9Bf',
           whale_acc,
          100000000000000))
