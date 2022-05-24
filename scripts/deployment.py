from scripts.utils import deploy_nft




def main():
    print("Will deploy NFT contract")
    try:
        deploy_nft()
        print("Successfully deployed")
    except:
        print("Error deploying")