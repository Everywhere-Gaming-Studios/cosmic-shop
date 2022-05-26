// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";


contract Marketplace is ReentrancyGuard{

    address payable public immutable feeAccount;
    uint public immutable feePercentage;
    uint itemCount;

    struct Item {
        uint itemId;
        IERC721 nftContract;
        uint tokenId;
        uint price;
        address payable seller;
        bool sold;
    }

    mapping(uint => Item) public items;


    event Offered(
        uint itemId,
        address indexed nft,
        uint tokenId,
        uint price,
        address indexed seller
    );

    event ItemPurchased(
        uint itemId,
        address indexed nft,
        uint tokenId,
        uint price,
        address indexed seller,
        address indexed buyer
    );

    constructor(uint _feePercent, address _feeAccount) {
        feeAccount = payable(_feeAccount);
        feePercentage = _feePercent;
    }


    function makeItem(IERC721 _nft, uint _tokenId, uint _price) external nonReentrant {
        require(_price > 0, "Price must be higher than zero");
        _nft.transferFrom(msg.sender, address(this), _tokenId);
        items[itemCount] = Item(itemCount,
        _nft,
        _tokenId,
        _price,
        payable(msg.sender),
        false);

        
        emit Offered(
            itemCount,
            address(_nft),
            _tokenId,
            _price,
            msg.sender
        );

        itemCount ++;

    }


    function purchaseItem(uint _itemId) external payable nonReentrant {
        uint _totalPrice = getTotalPrice(_itemId);
        Item storage item = items[_itemId];
        // Checks
        require(_itemId >= 0 && _itemId <= itemCount, "No such item listed");
        require(msg.value >= _totalPrice, "Not enough funds to cover for price and market fee");
        require(!item.sold, "Item not for sale anymore");  
        // Effects
        item.sold = true;      
        // Interactions
        payable(item.seller).call{value: item.price}("");
        payable(feeAccount).call{value:_totalPrice - item.price }("");
        item.nftContract.transferFrom(address(this), msg.sender, item.tokenId);
        emit ItemPurchased(_itemId, address(item.nftContract), item.tokenId, item.price, item.seller, msg.sender);
    }


    function getTotalPrice(uint _itemId) view public returns(uint) {
        return(items[_itemId].price*(100+feePercentage)/100);
    }

    function listItems() view public returns(Item[] memory) {
        Item[] memory itemsToReturn = new Item[](itemCount);
        for (uint i = 0; i < itemCount; i++) {
            Item storage item = items[i];
            itemsToReturn[i] = item;
        }
        return itemsToReturn;
    }


}