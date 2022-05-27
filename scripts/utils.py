from brownie import NFT, SimpleNFT, Marketplace, accounts, network, config
import os

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DEPLOY_ENV = os.getenv('DEPLOY_ENV')


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # Local ganache account
        account = accounts[0]
    else:
        print("Fetching credentials from live network")
        if DEPLOY_ENV == 'MAINNET':
            print("Fetching mainnet wallet")
            account = accounts.add(config["wallets"]["from_key"])
        else:
            print("Fetching testnet wallet")
            account = accounts.add(config["test_wallets"]["from_key"])
    return account



def deploy_nft():
    return NFT.deploy("Cosmic NFTs", "COSMICNFT", {"from": get_account()})


def deploy_marketplace():
    return Marketplace.deploy(1, get_account().address, {"from": get_account()})


def deploy_simple_nft():
    return SimpleNFT.deploy("Cosmic NFT", "COSMICNFT", {"from" : get_account()})