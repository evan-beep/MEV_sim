from decimal import Decimal
import json
import os
import time
from web3 import Web3
from web3.auto import w3
import requests
from eth_account import Account

from testing import calc_price, get_contract_abi
'''
ganache-cli --fork https://eth-mainnet.g.alchemy.com/v2/5K4nnjROFZ-KzwP-zW-kjclHNYN8E0sp --defaultBalanceEther 90000 --accounts=45 --account_keys_path /Users/EvanChen/project/web3/keys.json
'''

erc20_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'
pool_abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
router_abi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

# data of pools
pool_data = {
    'uniV2_router': {
        'address': Web3.to_checksum_address('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'),
        'abi': Web3.to_checksum_address('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
    },
    'uniV3_router': {
        'address': Web3.to_checksum_address('0xE592427A0AEce92De3Edee1F18E0157C05861564'),
        'abi': Web3.to_checksum_address('0xE592427A0AEce92De3Edee1F18E0157C05861564')
    },
    'univ2_factory': {
        'abi':  Web3.to_checksum_address(
            '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'),
        'address': Web3.to_checksum_address(
            '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'),
    },
    'weth': {
        'abi':  Web3.to_checksum_address(
            '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'),
        'address': Web3.to_checksum_address(
            '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'),
    },
    'usdt': {
        'abi':  Web3.to_checksum_address(
            '0xdAC17F958D2ee523a2206206994597C13D831ec7'),
        'address': Web3.to_checksum_address(
            '0xdAC17F958D2ee523a2206206994597C13D831ec7'),
    },
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
    'sushiswap_router': {
        'abi':  Web3.to_checksum_address(
            '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'),
        'address': Web3.to_checksum_address(
            '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'),
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

}
WETH_ADDRESS = pool_data['weth']['address']
USDT_ADDRESS = pool_data['usdt']['address']
POOL_ADDRESS = pool_data['uniswapV2_weth-usdt']['address']
ROUTER_ADDRESS = pool_data['uniV2_router']['address']


def check_allowance(web3, token_contract, owner_address, spender_address):
    allowance = token_contract.functions.allowance(
        owner_address, spender_address).call()
    return allowance


def check_router_contract(web3, router_address):
    router_contract = web3.eth.contract(
        address=router_address, abi=get_contract_abi(router_address))
    # Perform specific checks if needed, like checking the contract's code or methods
    return router_contract is not None


def get_v2_pool_price(reserve0, reserve1, decimals0, decimals1):
    amount0 = reserve0 / 10 ** decimals0
    amount1 = reserve1 / 10 ** decimals1

    return amount0 / amount1, amount1 / amount0


def check_token_balance(web3, token_address, account_address):
    token_contract = web3.eth.contract(
        address=token_address, abi=get_contract_abi(token_address))
    balance = token_contract.functions.balanceOf(account_address).call()
    return balance


def get_contract(web3, contract_name):

    contract = web3.eth.contract(
        address=pool_data[contract_name]['address'], abi=get_contract_abi(pool_data[contract_name]['abi']))
    return contract


def swap_token0_for_token1(web3, token0_address, token1_address, router_address,  account, amount_in_wei, slippage):
    # Create a contract instance for the Uniswap V2 Router
    uniswap_router = web3.eth.contract(
        address=router_address, abi=get_contract_abi(router_address))

    # Approve the Uniswap Router to spend WETH
    token0_contract = web3.eth.contract(address=token0_address, abi=get_contract_abi(
        token0_address))

    if token0_address == USDT_ADDRESS:
        approve_tx = token0_contract.functions.approve(router_address, amount_in_wei).build_transaction({
            'from': account['address'],
            'nonce': web3.eth.get_transaction_count(account['address']),
            'gas': 200000,
            'gasPrice': web3.to_wei('50', 'gwei')
        })
    else:
        approve_tx = token0_contract.functions.approve(router_address, amount_in_wei).build_transaction({
            'from': account['address'],
            'nonce': web3.eth.get_transaction_count(account['address'])
        })
    signed_approve_tx = web3.eth.account.sign_transaction(
        approve_tx, private_key=account['private_key'])
    web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
    web3.eth.wait_for_transaction_receipt(signed_approve_tx.hash)

    allowance = check_allowance(
        web3, token0_contract, account['address'], router_address)

    if allowance < amount_in_wei:
        raise Exception(
            "Approval failed, allowance is less than required amount. %s and %s" % (allowance, amount_in_wei))

    if not check_router_contract(web3, router_address):
        raise Exception("Invalid Router Contract.")

    token0_balance = check_token_balance(
        web3, token0_address, account['address'])
    if token0_balance < amount_in_wei:
        raise Exception("Insufficient token0 balance for the swap.")

    deadline = int(time.time()) + 600
    path = [token0_address, token1_address]
    amount_out_min = 0

    swap_txn = uniswap_router.functions.swapExactTokensForTokens(
        amount_in_wei,
        amount_out_min,
        path,
        account['address'],
        deadline
    ).build_transaction({
        'from': account['address'],
        'nonce': web3.eth.get_transaction_count(account['address']),
        'gas': 200000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })

    signed_swap_txn = web3.eth.account.sign_transaction(
        swap_txn, private_key=account['private_key'])
    tx_hash = web3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


def get_weth_balance(web3, account_address):
    weth_abi = get_contract_abi(WETH_ADDRESS)

    weth_contract = web3.eth.contract(
        address=WETH_ADDRESS, abi=weth_abi)

    # Get the balance
    balance_wei = weth_contract.functions.balanceOf(account_address).call()
    balance_weth = web3.from_wei(balance_wei, 'ether')

    return balance_weth


def get_usdt_balance(web3, account_address):
    usdt_abi = get_contract_abi(USDT_ADDRESS)

    usdt_contract = web3.eth.contract(
        address=USDT_ADDRESS, abi=usdt_abi)

    # Get the balance
    balance = usdt_contract.functions.balanceOf(account_address).call()
    balance_usdt = balance / (10**6)

    return balance_usdt


def send_transaction(web3_obj, from_address, to_address, amount):
    return web3_obj.eth.send_transaction({
        "from": from_address,
        "to": to_address,
        "value": amount
    })


def convert_eth_to_weth(web3, account_address, private_key, amount_in_wei):
    # Create contract instance for WETH
    weth_contract = web3.eth.contract(
        address=WETH_ADDRESS, abi=get_contract_abi(WETH_ADDRESS))

    # Build transaction to deposit ETH and convert it to WETH
    deposit_txn = weth_contract.functions.deposit().build_transaction({
        'from': account_address,
        'value': amount_in_wei,
        'gas': 200000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account_address),
    })

    signed_txn = web3.eth.account.sign_transaction(
        deposit_txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


def getPairAddress(web3, token0add, token1add, abi):
    factory_contract = web3.eth.contract(
        address=pool_data['univ2_factory']['address'], abi=abi)
    pair_address = factory_contract.functions.getPair(
        token0add, token1add).call()
    return pair_address


def transLog(web3, router, whale_input, my_input, fake_account, whale_account, ETHDiffList, WETHDiffList, pool, decimal0, decimal1):
    ROUTER = router

    eth_fake = web3
    # print(USING_POOL)

    initETH = 0
    initWETH = 0

    finalETH = 0
    finalWETH = 0

    eth_bal = Web3.to_wei(eth_fake.eth.get_balance(
        fake_account['address']), 'wei')*10**(-18)
    weth_bal = get_weth_balance(eth_fake, fake_account['address'])
    # print('initial ETH: %s, Initial WETH: %s, Initial Sum: %s' %
    #      (eth_bal, weth_bal, Decimal(str(eth_bal)) + weth_bal))
    initETH = eth_bal

    # reserve0, reserve1, _ = pool.functions.getReserves().call()
    # print('Init weth/usdt pool price: {}'.format(get_v2_pool_price(reserve0,
    #                                                               reserve1, decimals0, decimals1)))

    # get WETH
    convert_eth_to_weth(
        eth_fake, fake_account['address'], fake_account['private_key'], Web3.to_wei(my_input, 'ether'))
    eth_bal = Web3.to_wei(eth_fake.eth.get_balance(
        fake_account['address']), 'wei')*10**(-18)
    weth_bal = get_weth_balance(eth_fake, fake_account['address'])
    # print('After 10 ETH -> WETH, resulting ETH: %s, resulting WETH: %s' %
    #      (eth_bal, weth_bal))
    initWETH = weth_bal

    # print('Initial Pool price: %s' % calc_price(USING_POOL))

    # frontrunning

    swap_token0_for_token1(eth_fake, WETH_ADDRESS, USDT_ADDRESS,
                           ROUTER, fake_account, Web3.to_wei(my_input, 'ether'), 0.01)
    eth_bal = Web3.to_wei(eth_fake.eth.get_balance(
        fake_account['address']), 'wei')*10**(-18)
    weth_bal = get_weth_balance(eth_fake, fake_account['address'])

    # print('After swapping 10 WETH for USDT, resulting ETH: %s, resulting WETH: %s' %
    #      (eth_bal, weth_bal))

    # whale tx
    WHALE_TRANSAC_AMOUNT = whale_input
    convert_eth_to_weth(
        eth_fake, whale_account['address'], whale_account['private_key'], Web3.to_wei(WHALE_TRANSAC_AMOUNT, 'ether'))
    weth_bal = get_weth_balance(eth_fake, whale_account['address'])
    # print('whale buys usdt using %s weth' % weth_bal)
    swap_token0_for_token1(eth_fake, WETH_ADDRESS, USDT_ADDRESS,
                           ROUTER, whale_account, Web3.to_wei(WHALE_TRANSAC_AMOUNT, 'ether'), 0.01)

    # reserve0, reserve1, _ = pool.functions.getReserves().call()
    # print('Middle weth/usdt pool price: {}'.format(get_v2_pool_price(reserve0,
    #                                                                 reserve1, decimals0, decimals1)))

    # backrunning
    # print('USDT bal:%s' % get_usdt_balance(eth_fake, fake_account['address']))

    swap_token0_for_token1(eth_fake, USDT_ADDRESS, WETH_ADDRESS,
                           ROUTER, fake_account, int((10**6)*get_usdt_balance(eth_fake, fake_account['address'])), 0.01)
    eth_bal = Web3.to_wei(eth_fake.eth.get_balance(
        fake_account['address']), 'wei')*10**(-18)
    weth_bal = get_weth_balance(eth_fake, fake_account['address'])

    print('After swapping back from USDT to WETH, resulting ETH: %s, resulting WETH: %s, sum:%s' %
          (eth_bal, weth_bal, Decimal(str(eth_bal)) + weth_bal))

    finalETH = eth_bal
    finalWETH = weth_bal
    # print(calc_price(USING_POOL))

    # "reset" whale
    swap_token0_for_token1(eth_fake, USDT_ADDRESS, WETH_ADDRESS,
                           ROUTER, whale_account, int((10**6)*get_usdt_balance(eth_fake, whale_account['address'])), 0.01)
    # reserve0, reserve1, _ = pool.functions.getReserves().call()
    # print('Final weth/usdt pool price: {}'.format(get_v2_pool_price(reserve0,
    #                                                                reserve1, decimals0, decimals1)))

    ETHDiffList.append(finalETH-initETH)
    WETHDiffList.append(finalWETH-initWETH)


if __name__ == '__main__':

    node_fake = "http://127.0.0.1:8545"

    eth_fake = Web3(Web3.HTTPProvider(node_fake))

    weth = eth_fake.eth.contract(address=WETH_ADDRESS, abi=erc20_abi)
    usdt = eth_fake.eth.contract(address=USDT_ADDRESS, abi=erc20_abi)
    pool = eth_fake.eth.contract(address=POOL_ADDRESS, abi=pool_abi)
    router = eth_fake.eth.contract(address=ROUTER_ADDRESS, abi=router_abi)
    decimals0 = weth.functions.decimals().call()
    decimals1 = usdt.functions.decimals().call()

    ETHDiffList = []
    WETHDiffList = []

    with open('keys.json', 'r') as file:
        data = json.load(file)

    addresses = data['addresses']
    private_keys = data['private_keys']

    # Create list of dicts
    accounts_info = []
    for address in addresses:
        account_dict = {
            'address': Web3.to_checksum_address(address),
            'private_key': private_keys[address]
        }
        accounts_info.append(account_dict)

    all_fakes = accounts_info

    fake_account = accounts_info[0]
    whale_accounts = accounts_info[1:]

    print(eth_fake.is_connected())

    UNIV2_ROUTER = pool_data['uniV2_router']['address']
    SUSHI_ROUTER = pool_data['sushiswap_router']['address']

    factory_abi = get_contract_abi(pool_data['univ2_factory']['abi'])
    USING_POOL = getPairAddress(
        eth_fake, pool_data['weth']['address'], pool_data['usdt']['address'], factory_abi)

    for i in range(40):
        transLog(eth_fake, UNIV2_ROUTER, 100+500*i, 10, fake_account,
                 whale_accounts[i], ETHDiffList, WETHDiffList, pool, decimals0, decimals1)
        if i > 5:
            print(ETHDiffList)
            print(WETHDiffList)

    print(ETHDiffList)
    print(WETHDiffList)
