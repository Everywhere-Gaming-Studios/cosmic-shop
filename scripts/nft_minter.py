import json
from random import seed
from random import randint
# seed random number generator
seed(1)


def mint_withstandkairos_nfts(nft_contract, nft_info):
    nft_contract.mintWithstandKairosNFT(nft_info)


def list_nft_on_marketplace(marketplace):
    pass




def mint_and_list_nfts(marketplace=None, nft_contract=None):
    f = open('../automations/src/CosmicNFTsMetadata.json')
    data = json.load(f)
    for i, d in enumerate(data):
        tx = nft_contract.mintWithstandKairosNFT(d["metadataUri"], d["class"], d["rarity"])
        tx.wait(1) 
        approve_tx = nft_contract.approve(marketplace.address, i)
        approve_tx.wait(1)
        list_tx = marketplace.makeItem(nft_contract.address, i, (d["rarity"] + 1) * 10 ** 18, 2* (d["rarity"] + 1) * 10 ** 18, randint(1, 3))        
        list_tx.wait(1)

def main():
    mint_and_list_nfts()