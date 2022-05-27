// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./utils/Rarity.sol";


contract CollectibleNFT is HasRarity {

    enum CClasses { PROFILE_PIC, SKIN, MUSIC }

    // Props important for further logic
    struct CMetadata {
        string uri;
        CClasses class;
        Rarity rarity; // 0-4 (Normal- rare)
        uint index;
        // We may add more props as intended
    }

    mapping(uint => CMetadata) public cIndexMapping;

    uint[] cIds;

    function _setupCNFT(string memory _uri, uint8 _class, uint8 _rarity, uint id) internal {
        CClasses class = CClasses(_class); // This will automatically check whether this is legal or not
        Rarity rarity = Rarity(_rarity);
        cIndexMapping[id] = CMetadata(_uri, class, rarity, id); 
        cIds.push(id);
    }


    function _listCNFTs() internal view returns(CMetadata[] memory) {
            CMetadata[] memory cNFts = new CMetadata[](cIds.length);
            for (uint i = 0; i < cIds.length; i++) {
                cNFts[i] = cIndexMapping[i];
            }
            return cNFts;
    }
   
}