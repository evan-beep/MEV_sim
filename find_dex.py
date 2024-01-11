from web3 import Web3
from web3.auto import w3
import requests
from eth_account import Account

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
    'uniswap_wbtc-weth': {
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


def sqrt_price_x96_to_price(sqrt_price_x96, token0_decimals, token1_decimals):
    price0 = (sqrt_price_x96 / 2 ** 96) ** 2 * \
        10 ** (token0_decimals - token1_decimals)
    price1 = 1 / price0

    return price0, price1


def find_dex(dex, threshold):

    return


if __name__ == '__main__':
    whale_acc = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    node_fake = "http://127.0.0.1:8545"

    eth_fake = Web3(Web3.HTTPProvider(node_fake))
