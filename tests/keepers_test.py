import brownie
from tests_config import cosmic_nft, marketplace, account, investor, investor2, fee_collector, NFT_NAME, NFT_SYMBOL
from brownie import accounts, config, network
from utils import list_nft_on_marketplace, list_nft_ready_to_close_auction, nft_bid_start_price, compare_listed_nfts, duration_timestamp, nft_buyout_price
import eth_abi

def test_keeper(marketplace, account, cosmic_nft):
    list_nft_ready_to_close_auction(account, cosmic_nft, marketplace,0)
    list_nft_on_marketplace(account, cosmic_nft,marketplace, 1)
    list_nft_ready_to_close_auction(account, cosmic_nft, marketplace,2)
    result = marketplace.checkUpkeep(bytes(0))
    assert(eth_abi.decode_abi(["uint256[]"], result[1]) == ((0,2),))


def test_close_auction_without_bids(marketplace, account, cosmic_nft):
    list_nft_ready_to_close_auction(account, cosmic_nft, marketplace,0)
    assert(cosmic_nft.ownerOf(0)== marketplace.address)
    assert(len(marketplace.listItemsForSale()) == 1)
    result = marketplace.checkUpkeep(bytes(0))
    assert(result[0] == True and eth_abi.decode_abi(["uint256[]"], result[1]) == ((0,),))
    marketplace.performUpkeep(result[1])
    assert(cosmic_nft.ownerOf(0) == account.address)
    assert(len(marketplace.listItemsForSale()) == 0)

def test_close_auction_with_bids(marketplace, account, investor, cosmic_nft):
    
    initial_account_balance = account.balance()
    list_nft_on_marketplace(account, cosmic_nft, marketplace,0)
    list_nft_ready_to_close_auction(account, cosmic_nft, marketplace,1)
    fee = marketplace.getFee(1)
    marketplace.makeBidOnItem(1, {"from": investor, "value": nft_bid_start_price})
    result = marketplace.checkUpkeep(bytes(0))
    assert(eth_abi.decode_abi(["uint256[]"], result[1]) == ((1,),))
    marketplace.performUpkeep(result[1])
    assert(compare_listed_nfts(marketplace, 1, cosmic_nft.address, 1, nft_bid_start_price, 0, nft_buyout_price,account.address, (investor.address,nft_bid_start_price), True))
    assert(cosmic_nft.ownerOf(1) == investor.address)
    assert(account.balance() == initial_account_balance + nft_bid_start_price - fee)


