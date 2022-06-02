


# GLOBAL VARIABLES FOR TESTS
_uri= "test_uri"
_class = 1
_rarity = 3
nft_id = 0
nft_buyout_price = 100
nft_bid_start_price = 20
duration_timestamp = 60 * 60 
zero_address = '0x0000000000000000000000000000000000000000'

# UTIL FUNCTIONS
def list_nft_on_marketplace(account, cosmic_nft, marketplace, itemId):
    cosmic_nft.mintStage0Nft(_uri, _class, _rarity,{"from": account})
    cosmic_nft.approve(marketplace.address, itemId)
    marketplace.makeItem(cosmic_nft.address, itemId, nft_bid_start_price, nft_buyout_price, duration_timestamp, {"from": account})


def list_nft_ready_to_close_auction(account, cosmic_nft, marketplace, itemId):
    cosmic_nft.mintStage0Nft(_uri, _class, _rarity,{"from": account})
    cosmic_nft.approve(marketplace.address, itemId)
    marketplace.makeItem(cosmic_nft.address, itemId, nft_bid_start_price, nft_buyout_price, 0, {"from": account})


def compare_listed_nfts(marketplace, _itemId, _nft_address, _nft_id, _nft_bid_start_price, _duration_timestamp, _nft_buyout_price, _seller, _bid, _sold):
    listed_nft = marketplace.items(_itemId)
    if(listed_nft[0] != _itemId):
        return False
    elif(listed_nft[1] != _nft_address):
        return False
    elif(listed_nft[2] != _nft_id):
        return False
    elif(listed_nft[3] != _nft_bid_start_price):
        return False
    elif(listed_nft[4] != _duration_timestamp):
        return False
    elif(listed_nft[5] != _nft_buyout_price):
        return False
    elif(listed_nft[6] != _seller):
        return False
    elif(listed_nft[7] != _bid):
        return False
    elif(listed_nft[8] != _sold):
        return False

    return True
    
