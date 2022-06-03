const Moralis = require("moralis/node");
const {generateNFT, nftOptions, mintHero, listCosmicNFTs, rarities, wallet} = require('./utils/utils.js');
const {serverUrl, appId, masterKey, moralisSecret} = require('../config');
const { saveAllImages, mintAbunchOfNFTs } = require("./generateMetadataLinks.js");

console.log("Props: ", serverUrl, " ", appId, " ", masterKey, " ", moralisSecret);



async function startMoralisServer() {
    console.log("Starting Moralis");
    await Moralis.start({ serverUrl, appId, masterKey })
    // TODO find how to store png in base 64
  

 
    
}


startMoralisServer().then(async ()=>{
    mintAbunchOfNFTs();

})
