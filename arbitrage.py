from web3 import Web3, EthereumTesterProvider, AsyncWeb3
from eth_defi.uniswap_v3.pool import fetch_pool_details
from eth_abi import encode
import json
import requests
import time

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

weth_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "guy", "type": "address"},
            {"name": "wad", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "src", "type": "address"},
            {"name": "dst", "type": "address"},
            {"name": "wad", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "wad", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "dst", "type": "address"},
            {"name": "wad", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}, {"name": "", "type": "address"}],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {"payable": True, "stateMutability": "payable", "type": "fallback"},
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "src", "type": "address"},
            {"indexed": True, "name": "guy", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "src", "type": "address"},
            {"indexed": True, "name": "dst", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "dst", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Deposit",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "src", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Withdrawal",
        "type": "event",
    },
]

router_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_factory", "type": "address"},
            {"internalType": "address", "name": "_WETH9", "type": "address"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "inputs": [],
        "name": "WETH9",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes", "name": "path", "type": "bytes"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "amountOutMinimum",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct ISwapRouter.ExactInputParams",
                "name": "params",
                "type": "tuple",
            }
        ],
        "name": "exactInput",
        "outputs": [
            {"internalType": "uint256", "name": "amountOut", "type": "uint256"}
        ],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "tokenIn", "type": "address"},
                    {"internalType": "address", "name": "tokenOut", "type": "address"},
                    {"internalType": "uint24", "name": "fee", "type": "uint24"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "amountOutMinimum",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint160",
                        "name": "sqrtPriceLimitX96",
                        "type": "uint160",
                    },
                ],
                "internalType": "struct ISwapRouter.ExactInputSingleParams",
                "name": "params",
                "type": "tuple",
            }
        ],
        "name": "exactInputSingle",
        "outputs": [
            {"internalType": "uint256", "name": "amountOut", "type": "uint256"}
        ],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes", "name": "path", "type": "bytes"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "amountInMaximum",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct ISwapRouter.ExactOutputParams",
                "name": "params",
                "type": "tuple",
            }
        ],
        "name": "exactOutput",
        "outputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "tokenIn", "type": "address"},
                    {"internalType": "address", "name": "tokenOut", "type": "address"},
                    {"internalType": "uint24", "name": "fee", "type": "uint24"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "amountInMaximum",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint160",
                        "name": "sqrtPriceLimitX96",
                        "type": "uint160",
                    },
                ],
                "internalType": "struct ISwapRouter.ExactOutputSingleParams",
                "name": "params",
                "type": "tuple",
            }
        ],
        "name": "exactOutputSingle",
        "outputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "factory",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes[]", "name": "data", "type": "bytes[]"}],
        "name": "multicall",
        "outputs": [{"internalType": "bytes[]", "name": "results", "type": "bytes[]"}],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "refundETH",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "selfPermit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
            {"internalType": "uint256", "name": "expiry", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "selfPermitAllowed",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
            {"internalType": "uint256", "name": "expiry", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "selfPermitAllowedIfNecessary",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "selfPermitIfNecessary",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
            {"internalType": "address", "name": "recipient", "type": "address"},
        ],
        "name": "sweepToken",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "feeBips", "type": "uint256"},
            {"internalType": "address", "name": "feeRecipient", "type": "address"},
        ],
        "name": "sweepTokenWithFee",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "int256", "name": "amount0Delta", "type": "int256"},
            {"internalType": "int256", "name": "amount1Delta", "type": "int256"},
            {"internalType": "bytes", "name": "_data", "type": "bytes"},
        ],
        "name": "uniswapV3SwapCallback",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
            {"internalType": "address", "name": "recipient", "type": "address"},
        ],
        "name": "unwrapWETH9",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "feeBips", "type": "uint256"},
            {"internalType": "address", "name": "feeRecipient", "type": "address"},
        ],
        "name": "unwrapWETH9WithFee",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {"stateMutability": "payable", "type": "receive"},
]

w3 = Web3(EthereumTesterProvider())
"""
w3 = Web3(
    Web3.HTTPProvider("https://mainnet.infura.io/v3/c8499256051e4624a2bd7d551321db9f")
)
"""

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
A = w3.is_connected()
print("connected status : ", A)
# block = w3.eth.get_block(18869414)
# print(block)

# for tx_hash in block.transactions:
# tx = w3.eth.get_transaction(tx_hash)
# print(tx)


def sqrt_price_x96_to_price(sqrt_price_x96, token0_decimals=18, token1_decimals=18):
    price0 = (sqrt_price_x96 / 2**96) ** 2 * 10 ** (token0_decimals - token1_decimals)
    price1 = 1 / price0

    return price0, price1


"""
pool_contract_address = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
pool_details = fetch_pool_details(w3, pool_contract_address)
spot_price, tick, *_ = pool_details.pool.functions.slot0().call(
    block_identifier=18869414
)
print(spot_price)
price0, price1 = sqrt_price_x96_to_price(sqrt_price_x96=spot_price)
print(price0, price1)
"""


def get_pool_imformation(pool_contract_address, web3):
    pool_details = fetch_pool_details(web3, pool_contract_address)
    block = web3.eth.get_block("latest")
    print("block number = ", block.number)
    spot_price, tick, *_ = pool_details.pool.functions.slot0().call(
        block_identifier=block.number
    )
    print(
        "reserve : ",
    )
    price0, price1 = sqrt_price_x96_to_price(sqrt_price_x96=spot_price)
    print("price0 : ", price0, ",price1 : ", price1)


def get_funds(account, web3, money):
    whale_addr = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    # whale_addr = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    weth_contract = web3.eth.contract(
        address=web3.to_checksum_address(whale_addr), abi=ERC20_abi
    )

    symbol = weth_contract.functions.symbol().call()
    decimals = weth_contract.functions.decimals().call()
    totalSupply = weth_contract.functions.totalSupply().call() / 10**decimals
    addr_balance = weth_contract.functions.balanceOf(account).call() / 10**decimals

    # print("===== %s =====" % symbol)
    # print("decimal:", decimals)
    # print("Total Supply:", totalSupply)
    print("Before transfer, WETH Addr Balance:", addr_balance)

    weth_contract.functions.transfer(account, int(money * 10 ** (decimals))).transact(
        {
            "from": whale_addr,
        }
    )

    addr_balance = weth_contract.functions.balanceOf(account).call() / 10**decimals
    print("After transfer, WETH Addr Balance:", addr_balance)


def get_balance(account, token_address, web3):
    # only for ERC20 token
    token_contract = web3.eth.contract(
        address=web3.to_checksum_address(token_address), abi=ERC20_abi
    )
    decimals = token_contract.functions.decimals().call()
    addr_balance = token_contract.functions.balanceOf(account).call() / 10**decimals
    return addr_balance


def tran(account, router_address, web3, private_key):
    weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    MANA_address = "0x0F5D2fB29fb7d3CFeE444a200298f468908cC942"
    pool_address = "0x8661aE7918C0115Af9e3691662f605e9c550dDc9"  # Weth/MANA, 0.3%
    weth_contract = web3.eth.contract(
        address=web3.to_checksum_address(weth_address), abi=weth_ABI
    )

    MANA_contract = web3.eth.contract(
        address=web3.to_checksum_address(MANA_address), abi=ERC20_abi
    )

    print(
        "swap : ",
        weth_contract.functions.symbol().call(),
        "->",
        MANA_contract.functions.symbol().call(),
    )

    symbol = MANA_contract.functions.symbol().call()
    decimals = MANA_contract.functions.decimals().call()
    addr_balance = MANA_contract.functions.balanceOf(account).call() / 10**decimals
    fir_balance = addr_balance
    # print("===== %s =====" % symbol)
    # print("decimal:", decimals)
    # print("Before swap, MANA Addr Balance:", addr_balance)
    # print("uniswap V3 Weth/MANA imformation:")
    # get_pool_imformation(pool_address, web3)

    router_contract = web3.eth.contract(
        address=web3.to_checksum_address(router_address), abi=router_ABI
    )

    tx = weth_contract.functions.approve(router_address, 2**250).build_transaction(
        {"from": account, "nonce": 0}
    )
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # print("approve : ", tx_hash)

    myTrans = (
        weth_address,
        MANA_address,
        3000,
        account,
        2**200,
        10 * 10**18,
        0,
        0,
    )

    swp = router_contract.functions.exactInputSingle(myTrans).build_transaction(
        {
            "from": account,
            "nonce": 0,
        }
    )
    # print(swp)
    signed_swp = web3.eth.account.sign_transaction(
        swp, "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"
    )
    swp_hash = web3.eth.send_raw_transaction(signed_swp.rawTransaction)

    symbol = MANA_contract.functions.symbol().call()
    decimals = MANA_contract.functions.decimals().call()
    addr_balance = MANA_contract.functions.balanceOf(account).call() / 10**decimals
    sec_balance = addr_balance
    # print("===== %s =====" % symbol)
    # print("decimal:", decimals)
    # print("After swap, MANA Addr Balance:", addr_balance)
    # print("get: ", sec_balance - fir_balance)

    # print("uniswap V3 Weth/MANA imformation:")
    # get_pool_imformation(pool_address, web3)


def arb_tran(
    account, token0_address, token1_address, fee, router_address, web3, private_key
):
    token0_contract = web3.eth.contract(
        address=web3.to_checksum_address(token0_address), abi=weth_ABI
    )
    token1_contract = web3.eth.contract(
        address=web3.to_checksum_address(token1_address), abi=weth_ABI
    )
    router_contract = web3.eth.contract(
        address=web3.to_checksum_address(router_address), abi=router_ABI
    )

    print(
        "swap : ",
        token0_contract.functions.symbol().call(),
        "->",
        token1_contract.functions.symbol().call(),
    )

    # approve
    tx = token0_contract.functions.approve(router_address, 2**250).build_transaction(
        {"from": account, "nonce": 0}
    )
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # transaction
    decimals = token0_contract.functions.decimals().call()
    addr_balance = token0_contract.functions.balanceOf(account).call() / 10**decimals
    token0_balance = token0_contract.functions.balanceOf(account).call()

    while token0_balance > 0:
        small_swap = 2000 * 10**decimals
        if small_swap > token0_balance:
            small_swap = token0_balance

        myTrans = (
            token0_address,
            token1_address,
            fee,
            account,
            2**100,
            small_swap,
            0,
            0,
        )
        swp = router_contract.functions.exactInputSingle(myTrans).build_transaction(
            {
                "from": account,
                "nonce": 0,
            }
        )
        # print(swp)
        signed_swp = web3.eth.account.sign_transaction(swp, private_key)
        swp_hash = web3.eth.send_raw_transaction(signed_swp.rawTransaction)
        token0_balance = token0_contract.functions.balanceOf(account).call()
        # print("Token0 balance = ", token0_balance)


test_account = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
private_key = "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"
arb_account = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
arb_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"


weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
MANA_address = "0x0F5D2fB29fb7d3CFeE444a200298f468908cC942"
router_address = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
pool0_address = "0x8661aE7918C0115Af9e3691662f605e9c550dDc9"
pool1_address = "0xd9ed2b5f292a0e319a04e6c1aca15df97705821c"


# big trans
get_funds(test_account, w3, 500)
time.sleep(2)
for i in range(0, 20):  # send 20*10 weth
    print("i = ", i)
    tran(test_account, router_address, w3, private_key)  # weth->MANA, 0.3%
    get_pool_imformation(pool0_address, w3)
    time.sleep(1)
print("after big trans:")

get_pool_imformation(pool0_address, w3)
get_pool_imformation(pool1_address, w3)
# arb
print("before arbitrage, WETH = ", get_balance(arb_account, weth_address, w3))

get_funds(arb_account, w3, 1)
arb_tran(
    arb_account, weth_address, MANA_address, 10000, router_address, w3, arb_key
)  # WETH->MANA, 1%
get_pool_imformation(pool0_address, w3)
get_pool_imformation(pool1_address, w3)
print("buy many MANA =  ", get_balance(arb_account, MANA_address, w3))


arb_tran(
    arb_account, MANA_address, weth_address, 3000, router_address, w3, arb_key
)  # MANA->WETH, 0.3%

print("after arbitrage, WETH = ", get_balance(arb_account, weth_address, w3))
