// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


import "./utils/Rarity.sol";


contract Stage0NFT is HasRarity {

        enum S0Classes { AVATAR, WORKER, BUILDING, ITEMS, EQUIPMENT }

         // Props important for further logic
        struct S0Metadata {
            S0Classes class;
            Rarity rarity; // 0-4 (Normal- rare)
            uint index;
            // We may add more props as intended
        }

        mapping(uint => S0Metadata) public s0IndexMapping;

        uint[] public s0Ids;


        function _setupS0NFT(uint8 _class, uint8 _rarity, uint id) internal {
            S0Classes class = S0Classes(_class); // This will automatically check whether this is legal or not
            Rarity rarity = Rarity(_rarity);
            s0IndexMapping[id] = S0Metadata(class, rarity, id); 
            s0Ids.push(id);
        }


        function _listS0NFTs() internal view returns(S0Metadata[] memory) {
            S0Metadata[] memory s0NFts = new S0Metadata[](s0Ids.length);
            for (uint i = 0; i < s0Ids.length; i++) {
                s0NFts[i] = s0IndexMapping[i];
            }
            return s0NFts;
        }

}