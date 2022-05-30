// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";


contract Marketplace is ReentrancyGuard{

    enum PurchaseType {HIGHEST_BID, BUYOUT}

    address payable public immutable feeAccount;
    uint public immutable feePercentage;
    uint itemCount;

    struct Bid {
        address bidder;
        uint amount;
    }


    struct Item {
        uint itemId;
        IERC721 nftContract;
        uint tokenId;
        uint bidStartPrice;
        uint auctionEndTimestamp;
        uint buyoutPrice;
        address payable seller;
        Bid lastBid;
        bool sold;
    }

 
    mapping(uint => Item) public items;


    event Listed(
        uint itemId,
        address indexed nft,
        uint tokenId,
        uint bidStartPrice,
        uint auctionEndTimestamp,
        uint buyoutPrice,
        address indexed seller,
        uint timestamp
    );

    event BidRequest(
        uint itemId,
        address indexed bidder,
        uint amount,
        uint timestamp
    );

    event ItemPurchased(
        uint itemId,
        address indexed nft,
        uint tokenId,
        uint price,
        PurchaseType purhcaseType,
        address indexed seller,
        address indexed buyer,
        uint timestamp
    );

    constructor(uint _feePercent, address _feeAccount) {
        feeAccount = payable(_feeAccount);
        feePercentage = _feePercent;
    }


    function makeItem(IERC721 _nft, uint _tokenId, uint _bidStartPrice, uint _buyoutPrice, uint _endAuctionTimestamp) external nonReentrant {
        require(_buyoutPrice > 0, "Price must be higher than zero");
        _nft.transferFrom(msg.sender, address(this), _tokenId);
        items[itemCount] = Item(itemCount,
        _nft,
        _tokenId,
        _bidStartPrice,
        _endAuctionTimestamp,
        _buyoutPrice,
        payable(msg.sender),
        Bid(address(0),0),
        false);

        
        emit Listed(
            itemCount,
            address(_nft),
            _tokenId,
            _bidStartPrice,
            _endAuctionTimestamp,
            _buyoutPrice,
            msg.sender,
            block.timestamp
        );

        itemCount ++;

    }


    function buyoutItem(uint _itemId) external payable nonReentrant {
        uint _totalPrice = getTotalPrice(_itemId);
        Item storage item = items[_itemId];
        // Checks
        require(_itemId >= 0 && _itemId <= itemCount, "No such item listed");
        require(msg.value >= _totalPrice, "Not enough funds to cover for price and market fee");
        require(!item.sold, "Item not for sale anymore");  
        // Effects
        item.sold = true;      
        // Interactions
        payable(item.seller).call{value: item.buyoutPrice}("");
        payable(feeAccount).call{value:_totalPrice - item.buyoutPrice }("");
        item.nftContract.transferFrom(address(this), msg.sender, item.tokenId);
        emit ItemPurchased(
            _itemId,
            address(item.nftContract),
            item.tokenId,
            item.buyoutPrice,
            PurchaseType.BUYOUT,
            item.seller,
            msg.sender,
            block.timestamp
            );
    }

    // TODO lock funds and release after bid is overriden?????
    function makeBidOnItem(uint _itemId) external payable {
        uint _totalPrice = getTotalBidPrice(msg.value);
        Item storage item = items[_itemId];
        require(!item.sold, "Item not for sale anymore");  
        if(items[_itemId].lastBid.amount != 0) {
            require(msg.value >= item.bidStartPrice, "Amount provided is lower than minimum bid price");
        } else {
            require(msg.value >= item.bidStartPrice, "Amount provided is lower than last bid");
        }
        items[_itemId].lastBid.amount = msg.value;
        emit BidRequest(
            _itemId,
            msg.sender,
            msg.value,
            block.timestamp
            );
    }


    function getTotalPrice(uint _itemId) view public returns(uint) {
        return(items[_itemId].buyoutPrice*(100+feePercentage)/100);
    }

    function getTotalBidPrice(uint amount) view public returns(uint) {
        return(amount*(100+feePercentage)/100);
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