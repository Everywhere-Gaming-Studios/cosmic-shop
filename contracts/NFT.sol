// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "./Ownable.sol";

contract NFT is ERC721URIStorage, Ownable {

    // struct CosmicNft {
    //     string collection;
    //     // We may add more props as intended
    // }

    // mapping(string => uint[]) public collectionsMapping;

    // CosmicNft[] public cosmicNfts;

    uint public nftCount = 0;

    constructor (string memory _name, string memory _symbol) ERC721(_name,_symbol) {
        
    }

    function mint(string memory _uri) external onlyOwner {
        // cosmicNfts.push(CosmicNft(_collection));
        // collectionsMapping[_collection].push(cosmicNfts.length -1);
        _safeMint(msg.sender, nftCount);
        _setTokenURI(nftCount, _uri);
        nftCount++;
    }

    // function getCollectionElements(string memory _collection) public view returns (uint[] memory _collectionElements) {
    //     _collectionElements = collectionsMapping[_collection];
    // }


}