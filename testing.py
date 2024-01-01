import json
import requests
from web3 import Web3

# Connect to Ethereum blockchain
node_url = "https://eth-mainnet.g.alchemy.com/v2/5K4nnjROFZ-KzwP-zW-kjclHNYN8E0sp"
web3 = Web3(Web3.HTTPProvider(node_url))

# Ensure Web3 is connected
if not web3.is_connected():
    print("Failed to connect to Ethereum node.")
else:
    print("Successfully connected to Ethereum")


def get_contract_abi(contract_address):
    etherscan_api_key = 'IJY37SRWJ7E6Z6ZR3M3S9B8QSVZCSSE9PB'
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={etherscan_api_key}"

    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        return data['result']
    else:
        print(data)
        raise Exception("ABI not found or failed to fetch")


# data of pools
pool_data = {
    'uniswap_usdc-eth': {
        'abi':  Web3.to_checksum_address(
            '0x8f8EF111B67C04Eb1641f5ff19EE54Cda062f163'),
        'address': Web3.to_checksum_address(
            '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'),
        'token0_decimals': 6,
        'token1_decimals': 18
    },
    'uniswap_wbtc-eth': {
        'abi':  Web3.to_checksum_address(
            '0x8f8EF111B67C04Eb1641f5ff19EE54Cda062f163'),
        'address': Web3.to_checksum_address(
            '0xcbcdf9626bc03e24f779434178a73a0b4bad62ed'),
        'token0_decimals': 8,
        'token1_decimals': 18
    },
    'uniswapV2_eth-usdt': {
        'abi':  Web3.to_checksum_address(
            '0xC75650fe4D14017b1e12341A97721D5ec51D5340'),
        'address': Web3.to_checksum_address(
            '0x6C3e4cb2E96B01F4b866965A91ed4437839A121a'),
        'token0_decimals': 18,
        'token1_decimals': 6
    }
}

latest_block = 18769472  # eth.eth.block_number

interested_pool = pool_data['uniswap_wbtc-eth']

pool_abi = get_contract_abi(interested_pool['abi'])
pool_contract = web3.eth.contract(
    address=interested_pool['address'], abi=get_contract_abi(interested_pool['abi']))
reserves = pool_contract.functions.slot0().call(block_identifier=latest_block)
print(reserves)


def sqrt_price_x96_to_price(sqrt_price_x96, token0_decimals, token1_decimals):
    price0 = (sqrt_price_x96 / 2 ** 96) ** 2 * \
        10 ** (token0_decimals - token1_decimals)
    price1 = 1 / price0

    return price0, price1


print(sqrt_price_x96_to_price(
    reserves[0], interested_pool['token0_decimals'], interested_pool['token1_decimals']))
