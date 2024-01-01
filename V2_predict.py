from web3 import Web3

# Initialize Web3 and connect to Ethereum node
w3 = Web3(Web3.HTTPProvider('YOUR_PROVIDER_URL'))

# Uniswap V2 Pair Contract Address and ABI
uniswap_pair_contract_address = 'YOUR_UNISWAP_PAIR_CONTRACT_ADDRESS'
uniswap_pair_abi = 'YOUR_UNISWAP_PAIR_ABI'

# Create Contract Instance
uniswap_pair_contract = w3.eth.contract(
    address=uniswap_pair_contract_address, abi=uniswap_pair_abi)


def get_price_impact(amount_in, reserve_in, reserve_out):
    # adjusted for fee
    amount_in_with_fee = amount_in * 0.997
    new_reserve_in = reserve_in + amount_in_with_fee
    new_reserve_out = reserve_out - \
        (amount_in_with_fee * reserve_out) / new_reserve_in
    price_impact = ((reserve_out / reserve_in) -
                    (new_reserve_out / new_reserve_in)) * 100
    return price_impact


def main():
    # Fetch Current Reserves
    reserves = uniswap_pair_contract.functions.getReserves().call()
    reserve_a = reserves[0]
    reserve_b = reserves[1]
    amount_swapped = 100
    impact = get_price_impact(amount_swapped, reserve_a, reserve_b)
    print(f"Price impact of swapping {amount_swapped} tokens: {impact:.2f}%")


if __name__ == "__main__":
    main()
