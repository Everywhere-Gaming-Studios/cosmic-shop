from scripts.nft_minter import mint_and_list_nfts
from scripts.utils import deploy_nft, deploy_marketplace




def main():
    print("Will deploy NFT contract")
    try:
        nft_contract = deploy_nft()
        print("Successfully deployed")
    except:
        print("Error deploying")

    print("Deploying Marketplace")
    try:
         marketplace = deploy_marketplace()
         print("Marketplace successfully deployed")
    except:
        print("Error deploying marketplace")

    try:
        print("Will now mint and list NFTs")
        mint_and_list_nfts(marketplace, nft_contract)
    except Exception as e:
        print("Error miting NFTs: ", e)
