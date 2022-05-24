from brownie import NFT, Marketplace, accounts, network, config
from brownie.network import gas_price
from brownie.network.gas.strategies import GasNowStrategy
import pytest
import decorator
import os


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

NFT_NAME="NFT_TEST"
NFT_SYMBOL="NFTT"


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
def erc_721(account):
    return NFT.deploy(NFT_NAME, NFT_SYMBOL, {"from": account})


@pytest.fixture
def marketplace(account):
    return Marketplace.deploy(1, accounts[1], {"from": account})



