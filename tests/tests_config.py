from brownie import CosmicNFT, Marketplace, accounts, network, config
from brownie.network import gas_price
from brownie.network.gas.strategies import GasNowStrategy
import pytest
import decorator
import os


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

NFT_NAME="Cosmic NFT"
NFT_SYMBOL="COSMICNFT"


@pytest.fixture
def account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["test_wallets"]["from_key"])


@pytest.fixture
def investor():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[1]
    else:
        return accounts.add(config["test_wallets"]["from_key_2"])

@pytest.fixture
def investor2():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[2]
    else:
        return accounts.add(config["test_wallets"]["from_key_2"])



@pytest.fixture
def fee_collector():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[3]
    else:
        return accounts.add(config["test_wallets"]["from_key_2"])


@pytest.fixture
def cosmic_nft(account):
    return CosmicNFT.deploy(NFT_NAME, NFT_SYMBOL, {"from": account})


@pytest.fixture
def other_nft(account):
    return CosmicNFT.deploy("Other NFT", "OTHER", {"from": account})



@pytest.fixture
def marketplace(account, fee_collector, cosmic_nft):
    mktplc = Marketplace.deploy(1, fee_collector, {"from": account})
    mktplc.whitelistNftCollection(cosmic_nft.address, {"from": account})
    return mktplc

