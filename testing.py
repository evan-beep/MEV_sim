import json
import requests
from web3 import Web3

# Connect to Ethereum blockchain
node_url = "https://eth-mainnet.g.alchemy.com/v2/5K4nnjROFZ-KzwP-zW-kjclHNYN8E0sp"
web3 = Web3(Web3.HTTPProvider(node_url))
node_fake = "http://127.0.0.1:8545"

eth_fake = Web3(Web3.HTTPProvider(node_fake))

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
        'token1_decimals': 6,
        'v': 2
    },
    'sushiswap_weth-usdt': {
        'abi':  Web3.to_checksum_address(
            '0x06da0fd433C1A5d7a4faa01111c044910A184553'),
        'address': Web3.to_checksum_address(
            '0x06da0fd433C1A5d7a4faa01111c044910A184553'),
        'token0_decimals': 18,
        'token1_decimals': 6,
        'v': 2
    },
    'uniswapV3_weth-usdt': {
        'abi':  Web3.to_checksum_address(
            '0x4e68Ccd3E89f51C3074ca5072bbAC773960dFa36'),
        'address': Web3.to_checksum_address(
            '0x4e68Ccd3E89f51C3074ca5072bbAC773960dFa36'),
        'token0_decimals': 18,
        'token1_decimals': 6,
        'v': 3
    },
    'pancakeswap_weth-usdt': {
        'abi':  Web3.to_checksum_address(
            '0x17C1Ae82D99379240059940093762c5e4539aba5'),
        'address': Web3.to_checksum_address(
            '0x17C1Ae82D99379240059940093762c5e4539aba5'),
        'token0_decimals': 18,
        'token1_decimals': 6,
        'v': 2
    },
}

latest_block = 18769472  # eth.eth.block_number


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


def calc_price(interested_pool_name):
    try:
        interested_pool = pool_data[interested_pool_name]
    except:
        interested_pool = {
            'address': interested_pool_name,
            'abi': interested_pool_name,
            'v': 2,
            'token0_decimals': 18,
            'token1_decimals': 6
        }

    pool_contract = eth_fake.eth.contract(
        address=interested_pool['address'], abi=get_contract_abi(interested_pool['abi']))
    try:
        reserves = pool_contract.functions.slot0().call(block_identifier=latest_block)
    except:
        reserves = pool_contract.functions.getReserves().call(block_identifier=latest_block)

    if interested_pool['v'] == 2:
        return calculate_price_uniswap_v2(
            reserves[0], reserves[1], interested_pool['token0_decimals'], interested_pool['token1_decimals'])
    elif interested_pool['v'] == 3:
        return sqrt_price_x96_to_price(
            reserves[0], interested_pool['token0_decimals'], interested_pool['token1_decimals'])


if __name__ == "__main__":
    print(calc_price('sushiswap_weth-usdt'))
    print(calc_price('pancakeswap_weth-usdt'))
