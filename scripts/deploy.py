from brownie import FundMe, config, network
from .helpful_scripts import get_account, get_pricefeed


def deploy_fund_me():
    account = get_account()

    # Pass the price feed to our fundme contract
    # If we are on persistent network like rinkebym use the associated address
    # Otherwise use a mock  from the mockV3Aggregator contract
    price_feed = get_pricefeed()
    fund_me = FundMe.deploy(
        price_feed,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
