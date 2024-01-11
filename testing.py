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
    'uniswap_usdc-weth': {
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

    'uniswapV2_weth-usdt': {
        'abi':  Web3.to_checksum_address(
            '0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852'),
        'address': Web3.to_checksum_address(
            '0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852'),
        'token0_decimals': 18,
        'token1_decimals': 6
    },
    'sushiswap_weth-usdt': {
        'abi':  Web3.to_checksum_address(
            '0x06da0fd433C1A5d7a4faa01111c044910A184553'),
        'address': Web3.to_checksum_address(
            '0x06da0fd433C1A5d7a4faa01111c044910A184553'),
        'token0_decimals': 18,
        'token1_decimals': 6
    }
}

latest_block = 18769472  # eth.eth.block_number

interested_pool = pool_data['uniswapV2_weth-usdt']

pool_abi = get_contract_abi(interested_pool['abi'])
pool_contract = web3.eth.contract(
    address=interested_pool['address'], abi=get_contract_abi(interested_pool['abi']))
try:
    reserves = pool_contract.functions.slot0().call(block_identifier=latest_block)
except:
    reserves = pool_contract.functions.getReserves().call(block_identifier=latest_block)

print(reserves)


def calculate_price_uniswap_v2(reserve0, reserve1, token0_decimals, token1_decimals):
    # Adjust reserves for token decimals
    adjusted_reserve0 = reserve0 * (10 ** token1_decimals)
    adjusted_reserve1 = reserve1 * (10 ** token0_decimals)

    # Calculate prices
    price_of_token0_in_terms_of_token1 = adjusted_reserve1 / adjusted_reserve0
    price_of_token1_in_terms_of_token0 = adjusted_reserve0 / adjusted_reserve1

    return price_of_token0_in_terms_of_token1, price_of_token1_in_terms_of_token0


def sqrt_price_x96_to_price(sqrt_price_x96, token0_decimals, token1_decimals):
    price0 = (sqrt_price_x96 / 2 ** 96) ** 2 * \
        10 ** (token0_decimals - token1_decimals)
    price1 = 1 / price0

    return price0, price1


# print(sqrt_price_x96_to_price(
#    reserves[0], interested_pool['token0_decimals'], interested_pool['token1_decimals']))
print(calculate_price_uniswap_v2(
    reserves[0], reserves[1], interested_pool['token0_decimals'], interested_pool['token1_decimals']))
