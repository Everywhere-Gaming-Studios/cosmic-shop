import brownie
from tests_config import cosmic_nft, marketplace, account, investor,NFT_NAME, NFT_SYMBOL
from brownie import accounts, config, network



def test_make_item(account, cosmic_nft, marketplace):
    _uri= "test_uri"
    _class = 1
    _rarity = 3
    cosmic_nft.mintStage0Nft(_uri, _class, _rarity,{"from": account})
    nft_id = 0
    nft_price = 100
    cosmic_nft.approve(marketplace.address, 0)
    marketplace.makeItem(cosmic_nft.address, nft_id, nft_price, {"from": account})
    assert(marketplace.items(0) == (0, cosmic_nft.address, nft_id, nft_price, account.address, False))

def test_buyout_item(account, investor, cosmic_nft, marketplace):
    _uri= "test_uri"
    _class = 1
    _rarity = 3
    cosmic_nft.mintStage0Nft(_uri, _class, _rarity,{"from": account})
    nft_id = 0
    nft_price = 100
    cosmic_nft.approve(marketplace.address, 0)
    marketplace.makeItem(cosmic_nft.address, nft_id, nft_price, {"from": account})
    initial_balance = account.balance()
    price_to_pay = marketplace.getTotalPrice(0)
    marketplace.buyoutItem(0, {"from": investor, "value": price_to_pay})
    assert(account.balance() == initial_balance + nft_price)
    assert(cosmic_nft.ownerOf(0) == investor.address)


# Test make bid on item

# Test error bid with lower than minimum

# Test error bid with lower than last bid

# Test error bid already sold

# Test reentrancy

# Test List items

