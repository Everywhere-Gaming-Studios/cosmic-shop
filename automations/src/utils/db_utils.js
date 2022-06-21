const Moralis = require("moralis/node");


exports.saveNFTOnDb = function saveNFTOnDb({name, collection, _class, metadataUri, rarity}) {

    const NFTObject = Moralis.Object.extend("Test_NFTs");

    const nft = new NFTObject();

    console.log("Saving object on DB\n", {name,collection, rarity, metadataUri, _class});

    nft.set("name", name);
    nft.set("collection", collection);
    nft.set("rarity", rarity);
    nft.set("metadataURI", metadataUri);
    nft.set("class", _class);
    nft.save();

}