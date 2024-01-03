from web3 import Web3, EthereumTesterProvider, AsyncWeb3
from eth_defi.uniswap_v3.pool import fetch_pool_details

ERC20_abi = [
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


def get_funds(account, web3):
    whale_addr = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    weth_contract = web3.eth.contract(
        address=web3.to_checksum_address(whale_addr), abi=ERC20_abi
    )

    symbol = weth_contract.functions.symbol().call()
    decimals = weth_contract.functions.decimals().call()
    totalSupply = weth_contract.functions.totalSupply().call() / 10**decimals
    addr_balance = weth_contract.functions.balanceOf(account).call() / 10**decimals

    print("===== %s =====" % symbol)
    print("Total Supply:", totalSupply)
    print("Before transfer, Addr Balance:", addr_balance)

    weth_contract.functions.transfer(account, int(10 * 10 ** (decimals))).transact(
        {
            "from": whale_addr,
        }
    )

    addr_balance = weth_contract.functions.balanceOf(account).call() / 10**decimals
    print("After transfer, Addr Balance:", addr_balance)
