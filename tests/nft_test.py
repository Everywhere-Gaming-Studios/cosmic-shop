import brownie
from tests_config import cosmic_nft, marketplace, account, NFT_NAME, NFT_SYMBOL
from brownie import accounts, config, network



def test_nft_props(cosmic_nft):
    assert(cosmic_nft.name() == NFT_NAME)
    assert(cosmic_nft.symbol()== NFT_SYMBOL)

def test_mint(cosmic_nft, account):
    initial_balance = cosmic_nft.balanceOf(account.address) 
    assert(initial_balance == 0)
    _uri = "test_uri"
    _class = 0
    _rarity = 1
    cosmic_nft.mintStage0Nft(_uri, _class, _rarity,{"from": account})
    
    assert(cosmic_nft.balanceOf(account.address) == initial_balance + 1)

def test_get_colletion_elements(cosmic_nft, account):
    _minted_amount = 0
    _stage0_uri = "stage0_uri"
    _wk_uri = "wk_uri"
    _collectible_uri = "collectible_uri"
    _class = 1
    _rarity= 2
    cosmic_nft.mintStage0Nft(_stage0_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintWithstandKairosNFT(_wk_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintStage0Nft(_stage0_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintStage0Nft(_stage0_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintStage0Nft(_stage0_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintWithstandKairosNFT(_wk_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintWithstandKairosNFT(_wk_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintCollectibleNFT(_collectible_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintStage0Nft(_stage0_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintCollectibleNFT(_collectible_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    cosmic_nft.mintCollectibleNFT(_collectible_uri, _class, _rarity,{"from": account})
    _minted_amount+=1
    assert(cosmic_nft.getMintedAmount() == _minted_amount)
    nfts = cosmic_nft.listAllNFTs()
    # print("All nfts: ", nfts)
    stage0_nfts = nfts[0] 
    print("Stage 0 NFTs: ", stage0_nfts)
    wk_nfts = nfts[1] 
    print("Withstand Kairos NFTs: ", wk_nfts)
    collectible_nfts = nfts[2] 
    print("Collectible NFTs: ", collectible_nfts)
    assert(stage0_nfts[0][0] == _stage0_uri)
    assert(stage0_nfts[0][3] == 0)
    assert(wk_nfts[0][0] == _wk_uri)
    assert(collectible_nfts[0][0] == _collectible_uri)
    assert(collectible_nfts[-1][3] == _minted_amount -1)
    
        
def test_emitted_event_for_stage0(cosmic_nft, account):
    _uri = "test_uri"
    _class = 1
    _rarity= 2
    tx = cosmic_nft.mintStage0Nft(_uri, _class, _rarity,{"from": account})
    minting_event = tx.events['CosmicNftMinted']
    assert(minting_event['_collection'] == 'Stage0')
    assert(minting_event['_rarity'] == _rarity)
    assert(minting_event['_uri'] == _uri)
    assert(minting_event['_id'] == 0)
    assert(minting_event['_to'] == account.address)
    
    
def test_nft_ownership(cosmic_nft, account):
    _uri = "test_uri"
    _class = 1
    _rarity= 2
    cosmic_nft.mintStage0Nft(_uri, _class, _rarity,{"from": account})
    assert(cosmic_nft.ownerOf(0) == account.address)



