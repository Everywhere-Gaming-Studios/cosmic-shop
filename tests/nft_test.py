import brownie
from tests_config import erc_721, marketplace, account, NFT_NAME, NFT_SYMBOL
from brownie import accounts, config, network



def test_nft_props(erc_721):
    assert(erc_721.name() == NFT_NAME)
    assert(erc_721.symbol()== NFT_SYMBOL)

def test_mint(erc_721, account):
    initial_balance = erc_721.balanceOf(account.address) 
    assert(initial_balance == 0)

    erc_721.mint("test_uri", "rare")
    
    assert(erc_721.balanceOf(account.address) == initial_balance + 1)

def 