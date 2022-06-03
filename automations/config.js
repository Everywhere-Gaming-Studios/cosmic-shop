require('dotenv').config({path: __dirname + '/.env'});


console.log(process.env.NFT_ADDRESS);
module.exports = {
    nftAddress: process.env.NFT_ADDRESS,
    marketplaceAddress: process.env.MARKETPLACE_ADDRESS,
    serverUrl: process.env.SERVER_URL,
    appId: process.env.APPLICATION_ID,
    privateKey:process.env.TESTNET_PRIVATE_KEY,
    masterKey: process.env.MASTER_KEY,
    moralisSecret: process.env.MORALIS_SECRET,
    speedyNodeUrl:process.env.SPEEDY_NODE_URL


}