from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork- dev"]

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "ganache-local_bis"]


DECIMALS = 10
STARTING_PRICE = 2000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() not in FORKED_LOCAL_ENVIRONMENTS
    ):
        # print(*accounts)
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_pricefeed():
    print(f"The active network is{network.show_active()}")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        return price_feed_address
    print("Deploying Mocks...")
    account = get_account()
    if len(MockV3Aggregator) <= 0:

        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": account}
        )
    print("Mocks Deployed!")
    price_feed_address = MockV3Aggregator[
        -1
    ].address  # Contract[-1] gets the latest deployed version of a contract
    return price_feed_address
