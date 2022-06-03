const ABIs = require('../ABIs.js');
const ethers = require('ethers');
const saveMetadataOnIPFS = require('./ipfs_utils');
const cosmicNftAbi = ABIs.cosmicNftAbi;
const{ nftAddress, marketplaceAddress, speedyNodeUrl, privateKey} = require('../../config'); 


console.log("Connecting to node: ", speedyNodeUrl);
const provider = new ethers.providers.JsonRpcProvider(speedyNodeUrl);
const wallet = new ethers.Wallet(privateKey, provider);

const nftContract = new ethers.Contract(nftAddress, cosmicNftAbi, wallet);


const Stage0Classes = Object.freeze({AVATAR:0, WORKER:1, BUILDING:2, ITEMS:3, EQUIPMENT:4})

const WithstandKairosClasses = Object.freeze({HERO:0, COMPANION:1, TROOP:2, TOWER:3, BARRIER:4, POTIONS:5, FOOD:6})

const CollectibleClasses = Object.freeze({PROFILE_PIC: 0, SKIN: 1, MUSIC: 2})


exports.wallet = wallet;



const mintStage0NFT = async (_name, _type, _class, _rarity) => {
    
    const uri = await saveMetadataOnIPFS(_name, _type, 'Stage0', _class, _rarity);
    console.log("Minting NFT with uri ", uri);
    const tx = await nftContract.mintStage0Nft(uri, _class, _rarity, {from: wallet.address, gasLimit: 230000});
    console.log("NFT successfully minted!!")
    const receipt = await tx.wait(2);


    return receipt;
}


exports.mintHero = async(_name, _rarity) => {
    return await mintStage0NFT(_name, "withstandKairos", WithstandKairosClasses.HERO, _rarity);
}

exports.simpleMint = async () => {
    const tx = await nftContract.mintStage0Nft("Test", 1,2, {from: wallet.address, gasLimit: 230000});
    const receipt = await tx.wait(2);
    return receipt;
}

exports.getOwner = async () => {
    const owner = await nftContract.owner();
    return owner;
}


exports.listCosmicNFTs = async () => {
    return await nftContract.getMintedAmount();
}



exports.rarities = Object.freeze({ NORMAL:0, RARE:1, EPIC:2, LEGENDARY:3, COSMIC: 4})
