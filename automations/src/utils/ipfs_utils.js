const fs = require('fs');
const Moralis = require("moralis/node");


const btoa = function (str) {
    return Buffer.from(str).toString("base64");
};


exports.saveImageOnIPFS = async (_asset_type, _asset_name) => {

    console.log("Saving metadata to IPFS...");
    const img = fs.readFileSync(`./assets/${_asset_type}/${_asset_name}.png`)
    const imageFile = new Moralis.File('img.png', {base64: btoa(img)})

    const savedImage = await imageFile.saveIPFS({useMasterKey: true});

    const image_uri = await savedImage.ipfs();

    return image_uri;

}

// TODO guardar também na DB do Moralis
module.saveMetadataOnIPFS = async (_imageUri, _asset_name, _asset_type, _collection,_class, _rarity) => {
    

    console.log("Merging and saving metadata...")
    const obj = {name: _name, collection: _collection, class: _class, rarity: _rarity, image_uri: _imageUri}
    const file = new Moralis.File("obj.json", { base64: btoa(JSON.stringify(obj))});
    const savedObject = await file.saveIPFS({useMasterKey: true});
    const uri = await savedObject.ipfs();
    console.log(`Metadata successfully saved with uri ${uri}`)
    return uri;

}