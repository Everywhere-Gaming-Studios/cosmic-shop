import brownie
from tests_config import cosmic_nft, marketplace, account, investor, investor2, fee_collector, NFT_NAME, NFT_SYMBOL
from brownie import accounts, config, network
from utils import list_nft_on_marketplace, compare_listed_nfts, nft_id, nft_buyout_price, duration_timestamp, nft_bid_start_price, zero_address



# TESTS

def test_make_item(account, cosmic_nft, marketplace):
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, nft_id, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address, (zero_address,0), False))
    assert(len(marketplace.listItemsForSale()) == 1)



def test_items_for_sale_management(account, cosmic_nft, investor, marketplace):
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    list_nft_on_marketplace(account, cosmic_nft, marketplace,1)
    list_nft_on_marketplace(account, cosmic_nft, marketplace,2)
    list_nft_on_marketplace(account, cosmic_nft, marketplace,3)
    list_nft_on_marketplace(account, cosmic_nft, marketplace,4)
    marketplace.buyoutItem(1, {"from": investor, "value": nft_buyout_price})
    assert(marketplace.listItemsForSale()==(0,4,2,3))
    


def test_make_item_not_owned_by_address(account, cosmic_nft, marketplace):
    pass


def test_buyout_item(account, investor, fee_collector, cosmic_nft, marketplace):
    
    # List item on marketplace
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    
    fee = marketplace.getFee(0)
    # Initial balance state
    initial_balance = account.balance()
    investor_initial_balance = investor.balance()
    fee_collector_initial_balance = fee_collector.balance()
    price_to_pay = nft_buyout_price
    
    #Buyout action
    marketplace.buyoutItem(0, {"from": investor, "value": price_to_pay})
    
    #Assertions
    assert(account.balance() == initial_balance + nft_buyout_price - fee) # Seller final balance 
    assert(cosmic_nft.ownerOf(0) == investor.address) # Owner after buyout is now investor
    assert(investor.balance() == investor_initial_balance - price_to_pay) # Investor final balance
    assert(fee_collector.balance() == fee_collector_initial_balance + fee) # Fee collector final balance
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, 0, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address, (zero_address,0), True))



# Test make bid on item
def test_bid_on_item(account, investor, cosmic_nft, marketplace):
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    initial_balance = investor.balance()
    marketplace.makeBidOnItem(0, {"from": investor, "value": nft_bid_start_price})
    assert(investor.balance() == initial_balance - nft_bid_start_price)
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, nft_id, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address, (investor,nft_bid_start_price), False))
    


def test_subsequent_bid(account, investor, investor2, cosmic_nft, marketplace):
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    initial_balance = investor.balance()
    new_investor_initial_balance = investor2.balance()
    marketplace.makeBidOnItem(0, {"from": investor, "value": nft_bid_start_price})
    assert(investor.balance() == initial_balance - nft_bid_start_price)    
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, nft_id, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address,(investor.address,nft_bid_start_price), False))

    
    marketplace.makeBidOnItem(0, {"from": investor2, "value": nft_bid_start_price + 1})
    assert(investor.balance() == initial_balance)    
    assert(investor2.balance() == new_investor_initial_balance - nft_bid_start_price -1)    
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, nft_id, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address, (investor2.address,nft_bid_start_price + 1), False))
    

def test_auto_buyout_for_bids_higher_than_buyout_price(account, investor, investor2, fee_collector, cosmic_nft, marketplace):
    
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    fee = marketplace.getFee(0)

    initial_balance = investor.balance()
    seller_initial_balance = account.balance()
    new_investor_initial_balance = investor2.balance()
    fee_collector_initial_balance= fee_collector.balance()
    marketplace.makeBidOnItem(0, {"from": investor, "value": nft_bid_start_price})
    assert(investor.balance() == initial_balance - nft_bid_start_price)
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, nft_id, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address, (investor.address,nft_bid_start_price), False))
    
    marketplace.makeBidOnItem(0, {"from": investor2, "value": nft_bid_start_price + 1})
    assert(investor.balance() == initial_balance)    
    assert(investor2.balance() == new_investor_initial_balance - nft_bid_start_price -1)    
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, nft_id, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address, (investor2.address,nft_bid_start_price + 1), False))

    marketplace.makeBidOnItem(0, {"from": investor2, "value": nft_buyout_price})

    #Assertions
    assert(account.balance() == seller_initial_balance + nft_buyout_price - fee) # Seller final balance 
    assert(cosmic_nft.ownerOf(0) == investor2.address) # Owner after buyout is now investor
    assert(investor2.balance() == new_investor_initial_balance - nft_buyout_price) # Investor final balance
    assert(fee_collector.balance() == fee_collector_initial_balance + fee) # Fee collector final balance
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, nft_id, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address, (investor2.address,nft_buyout_price), True))


def test_bid_close(account, investor, investor2, fee_collector, cosmic_nft, marketplace):
    pass




# ------------------------------------ REVERTS -------------------------------------------

def test_revert_for_bid_from_seller(account, cosmic_nft, marketplace):
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    with brownie.reverts("Seller is not allowed to make bids"):
        marketplace.makeBidOnItem(0, {"from": account, "value": nft_bid_start_price})


def test_revert_for_bid_smaller_than_minimum(account, investor, cosmic_nft, marketplace):
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    with brownie.reverts("Amount provided is lower than minimum bid price"):
        marketplace.makeBidOnItem(0, {"from": investor, "value": nft_bid_start_price - 1})


def test_revert_for_equal_bid(account, investor, investor2, cosmic_nft, marketplace):
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    initial_balance = investor.balance()
    marketplace.makeBidOnItem(0, {"from": investor, "value": nft_bid_start_price})
    assert(investor.balance() == initial_balance - nft_bid_start_price)    
    assert(compare_listed_nfts(marketplace, 0, cosmic_nft.address, nft_id, nft_bid_start_price, duration_timestamp, nft_buyout_price,account.address, (investor.address,nft_bid_start_price), False))

    with brownie.reverts("Amount provided is lower or equal to last bid"):
        marketplace.makeBidOnItem(0, {"from": investor2, "value": nft_bid_start_price})
    




# Test error bid with lower than minimum


# Test error bid already sold

# Test reentrancy

# Test List items

