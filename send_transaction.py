import time
from web3 import Web3
from web3.auto import w3
import requests
from eth_account import Account

from testing import calc_price, get_contract_abi
'''
ganache-cli --fork https://eth-mainnet.g.alchemy.com/v2/5K4nnjROFZ-KzwP-zW-kjclHNYN8E0sp -- unlock 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
'''

# data of pools
pool_data = {
    'uniV2_router': {
        'address': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
        'abi': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
    },
    'weth': {
        'abi':  Web3.to_checksum_address(
            '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'),
        'address': Web3.to_checksum_address(
            '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'),
    },
    'usdc': {
        'abi':  Web3.to_checksum_address(
            '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'),
        'address': Web3.to_checksum_address(
            '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'),
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


def check_allowance(web3, token_contract, owner_address, spender_address):
    allowance = token_contract.functions.allowance(
        owner_address, spender_address).call()
    return allowance


def check_router_contract(web3, router_address):
    router_contract = web3.eth.contract(
        address=router_address, abi=get_contract_abi(router_address))
    # Perform specific checks if needed, like checking the contract's code or methods
    return router_contract is not None


def check_token_balance(web3, token_address, account_address):
    token_contract = web3.eth.contract(
        address=token_address, abi=get_contract_abi(token_address))
    balance = token_contract.functions.balanceOf(account_address).call()
    return balance


def get_contract(web3, contract_name):

    contract = web3.eth.contract(
        address=pool_data[contract_name]['address'], abi=get_contract_abi(pool_data[contract_name]['abi']))
    return contract


def swap_weth_for_usdc(web3, weth_address, usdc_address, router_address,  account_address, amount_in_wei, slippage):
    # Create a contract instance for the Uniswap V2 Router
    uniswap_router = web3.eth.contract(
        address=router_address, abi=get_contract_abi(router_address))

    # Approve the Uniswap Router to spend WETH
    weth_contract = web3.eth.contract(address=weth_address, abi=get_contract_abi(
        weth_address))  # Assume weth_abi is already defined
    approve_tx = weth_contract.functions.approve(router_address, amount_in_wei).build_transaction({
        'from': account_address['address'],
        'nonce': web3.eth.get_transaction_count(account_address['address'])
    })
    signed_approve_tx = web3.eth.account.sign_transaction(
        approve_tx, private_key=account_address['private_key'])
    web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
    web3.eth.wait_for_transaction_receipt(signed_approve_tx.hash)

    allowance = check_allowance(
        web3, weth_contract, account_address['address'], router_address)

    if allowance < amount_in_wei:
        raise Exception(
            "Approval failed, allowance is less than required amount.")

    if not check_router_contract(web3, router_address):
        raise Exception("Invalid Router Contract.")

    weth_balance = check_token_balance(
        web3, weth_address, account_address['address'])
    if weth_balance < amount_in_wei:
        raise Exception("Insufficient WETH balance for the swap.")

    # Set the parameters for the swap
    # Transaction deadline (10 minutes from now)
    deadline = int(time.time()) + 600
    path = [weth_address, usdc_address]
    amount_out_min = 0  # Set to 0 for simplicity, but should be calculated based on slippage

    # Build the swap transaction
    swap_txn = uniswap_router.functions.swapExactTokensForTokens(
        amount_in_wei,
        amount_out_min,
        path,
        account_address['address'],
        deadline
    ).build_transaction({
        'from': account_address['address'],
        'nonce': web3.eth.get_transaction_count(account_address['address']),
        'gas': 200000,  # Set an appropriate gas limit
        'gasPrice': web3.to_wei('50', 'gwei')  # Set an appropriate gas price
    })

    # Sign and send the transaction
    signed_swap_txn = web3.eth.account.sign_transaction(
        swap_txn, private_key=account_address['private_key'])
    tx_hash = web3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)

    # Wait for the transaction to be mined
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


def send_transaction(web3_obj, from_address, to_address, amount):
    return web3_obj.eth.send_transaction({
        "from": from_address,
        "to": to_address,
        "value": amount
    })


def convert_eth_to_weth(web3, account_address, private_key, amount_in_wei):
    # Create contract instance for WETH
    weth_contract = web3.eth.contract(
        address=pool_data['weth']['address'], abi=get_contract_abi(pool_data['weth']['abi']))

    # Build transaction to deposit ETH and convert it to WETH
    deposit_txn = weth_contract.functions.deposit().build_transaction({
        'from': account_address,
        'value': amount_in_wei,  # Amount of ETH to convert to WETH
        'gas': 200000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account_address),
    })

    # Sign and send the transaction
    signed_txn = web3.eth.account.sign_transaction(
        deposit_txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


if __name__ == '__main__':
    whale_acc = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    node_fake = "http://127.0.0.1:8545"

    eth_fake = Web3(Web3.HTTPProvider(node_fake))

    fake_account = {
        'address': Web3.to_checksum_address('0x5e355c989d2810EB53AAA9dE6d07e6A8FCBC517F'),
        'private_key': '0x739bc8a973a7fb95ec0ab4276c227d22ba1d9544016e222536b720286ed394f0'
    }
    print(eth_fake.is_connected())

    amount_in = Web3.to_wei(0.1, 'ether')  # Convert 0.1 WETH to Wei
    # Example rate, this should be obtained from a current market source
    weth_usdc_rate = 200
    slippage = 0.01  # 1%

    convert_eth_to_weth(
        eth_fake, fake_account['address'], fake_account['private_key'], Web3.to_wei(1, 'ether'))

    print(eth_fake.eth.get_balance(fake_account['address']))
    print(swap_weth_for_usdc(eth_fake, pool_data['weth']['address'],
                             pool_data['usdc']['address'], pool_data['uniV2_router']['address'], fake_account, amount_in, 0.05))
