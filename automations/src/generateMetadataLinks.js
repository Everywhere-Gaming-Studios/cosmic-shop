const { saveImageOnIPFS } = require("./utils/ipfs_utils");
const { rarities } = require("./utils/utils");
const fs = require('fs');

const heroeAssetName = 'withstandKairos';

const heroesNames = ['Healer','Tank','Ranger', 'Pioneer', 'Samurai','Mage'];

const WithstandKairosClasses = Object.freeze({HERO:0, COMPANION:1, TROOP:2, TOWER:3, BARRIER:4, POTIONS:5, FOOD:6})


let imageUris =JSON.parse(fs.readFileSync('./ImageUris.json'));


exports.saveAllImages = async function saveAllImages() {
    
    const imageUris = [];
    await Promise.all(heroesNames.map(async (h)=> {
        const uri = await saveImageOnIPFS(heroeAssetName, h)
        imageUris.push({hero: h, imageUri: uri});
    }))
    
    
    console.log("Received uris: ", imageUris);
    const data = JSON.stringify(imageUris);
    fs.writeFileSync('ImageUris.json', data);
}



exports.mintAbunchOfNFTs = async function mintAbunchOfNFTs(){

    for (let i=0; i< imageUris.length; i++) {
        console.log(imageUris[i]);
    }



}