import brownie
from tests_config import erc_721, marketplace, account, investor,NFT_NAME, NFT_SYMBOL
from brownie import accounts, config, network



def test_make_item(account, erc_721, marketplace):
    erc_721.mint("test_uri", {"from": account})
    nft_id = 0
    nft_price = 100
    erc_721.approve(marketplace.address, 0)
    marketplace.makeItem(erc_721.address, nft_id, nft_price, {"from": account})
    assert(marketplace.items(0) == (0, erc_721.address, nft_id, nft_price, account.address, False))

def test_purchase_item(account, investor, erc_721, marketplace):
    erc_721.mint("test_uri",{"from": account})
    nft_id = 0
    nft_price = 100
    erc_721.approve(marketplace.address, 0)
    marketplace.makeItem(erc_721.address, nft_id, nft_price, {"from": account})
    initial_balance = account.balance()
    price_to_pay = marketplace.getTotalPrice(0)
    marketplace.purchaseItem(0, {"from": investor, "value":price_to_pay})
    assert(account.balance() == initial_balance + nft_price)
    assert(erc_721.ownerOf(0) == investor.address)


# Test reentrancy

# Test List items

