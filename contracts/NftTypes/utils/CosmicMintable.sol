pragma solidity ^0.8.0;

import "./Rarity.sol";

contract CosmicMintable is HasRarity {

    event CosmicNftMinted (string _collection, Rarity _rarity, string _uri, uint _id, address _to);

}