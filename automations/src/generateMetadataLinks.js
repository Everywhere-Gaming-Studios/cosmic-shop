const { saveImageOnIPFS, saveMetadataOnIPFS } = require("./utils/ipfs_utils");
const { rarities } = require("./utils/utils");
const fs = require('fs');
const { saveNFTOnDb } = require("./utils/db_utils");

const collection = 'withstandKairos';

const heroesNames = ['Healer','Tank','Ranger', 'Pioneer', 'Samurai','Mage'];

const WithstandKairosClasses = Object.freeze({HERO:0, COMPANION:1, TROOP:2, TOWER:3, BARRIER:4, POTIONS:5, FOOD:6})


let imageUris =JSON.parse(fs.readFileSync('./ImageUris.json'));



exports.saveAllImages = async function saveAllImages() {
    
    const imageUris = [];
    await Promise.all(heroesNames.map(async (h)=> {
        const uri = await saveImageOnIPFS(collection, h)
        imageUris.push({hero: h, imageUri: uri});
    }))
    
    
    console.log("Received uris: ", imageUris);
    const data = JSON.stringify(imageUris);
    fs.writeFileSync('ImageUris.json', data);
}



exports.mintAbunchOfNFTs = async function mintAbunchOfNFTs(){

    const finalNFTs = [];

    const heroesToMint = [...heroesNames, ...heroesNames, ...heroesNames, ...heroesNames];

    const class_ = WithstandKairosClasses.HERO;

    await Promise.all(heroesToMint.map(async (h, i)=> {
        let rarity = Math.floor(Math.random() * 4);

        try{
            const imageUri = await saveImageOnIPFS(collection, h);
            console.log("Successfully saved image for ", h);
            const metadataUri = await saveMetadataOnIPFS(imageUri, h,collection, class_, rarity);
            console.log("Successfully saved metadata for ", h, "( "+i +")");
            await saveNFTOnDb({name: h, collection,  _class: class_, metadataUri, rarity});
            console.log("Successfully saved on db ", h, "( "+i +")");
            finalNFTs.push({metadataUri: metadataUri, class: class_, rarity})
        } catch (e) {
            console.log("Error on hero ", h , "(" ,i,")", " error is: ", e);
        }
    }))

    const data = JSON.stringify(finalNFTs);
    fs.writeFileSync('CosmicNFTsMetadata.json', data);

}