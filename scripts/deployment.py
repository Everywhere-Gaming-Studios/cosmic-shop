from scripts.utils import deploy_nft, deploy_marketplace




def main():
    print("Will deploy NFT contract")
    try:
        deploy_nft()
        print("Successfully deployed")
    except:
        print("Error deploying")

    print("Deploying Marketplace")
    try:
         deploy_marketplace()
         print("Marketplace successfully deployed")
    except:
        print("Error deploying marketplace")