const fs = require('fs');
const Moralis = require("moralis/node");


const btoa = function (str) {
    return Buffer.from(str).toString("base64");
};


exports.saveImageOnIPFS = async (_asset_type, _asset_name) => {

    const img = fs.readFileSync(`./assets/${_asset_type}/${_asset_name}_background.jpg`)
    const imageFile = new Moralis.File(`img.jpg`, {base64: btoa(img)})

    const savedImage = await imageFile.saveIPFS({useMasterKey: true});

    const image_uri = await savedImage.ipfs();

    return image_uri;

}

// TODO guardar também na DB do Moralis
exports.saveMetadataOnIPFS = async (_imageUri, _name, _collection,_class, _rarity) => {
    

    const obj = {name: _name, collection: _collection, class: _class, rarity: _rarity, image_uri: _imageUri}
    const file = new Moralis.File("obj.json", { base64: btoa(JSON.stringify(obj))});
    const savedObject = await file.saveIPFS({useMasterKey: true});
    const uri = await savedObject.ipfs();
    return uri;

}