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
        uint auctionDuration;
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
        uint auctionDuration,
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


    function makeItem(IERC721 _nft, uint _tokenId, uint _bidStartPrice, uint _buyoutPrice, uint _auctionDuration) external nonReentrant {
        
        require(_buyoutPrice > 0, "Price must be higher than zero");
        
        _nft.transferFrom(msg.sender, address(this), _tokenId);

        items[itemCount] = Item(itemCount,
        _nft,
        _tokenId,
        _bidStartPrice,
        _auctionDuration,
        _buyoutPrice,
        payable(msg.sender),
        Bid(address(0),0),
        false);

        emit Listed(
            itemCount,
            address(_nft),
            _tokenId,
            _bidStartPrice,
            _auctionDuration,
            _buyoutPrice,
            msg.sender,
            block.timestamp
        );

        itemCount ++;

    }


    function buyoutItem(uint _itemId) external payable nonReentrant {
        _processBuyout(_itemId, msg.value);
    }

    // TODO lock funds and release after bid is overriden?????
    function makeBidOnItem(uint _itemId) external payable nonReentrant {
        
        Item storage item = items[_itemId];
        require(msg.sender != item.seller, "Seller is not allowed to make bids");
        require(!item.sold, "Item not for sale anymore");  
        if(item.lastBid.amount == 0) { // First bid
            require(msg.value >= item.bidStartPrice, "Amount provided is lower than minimum bid price");
        } else { // Subsequent bids
            require(msg.value > item.lastBid.amount, "Amount provided is lower or equal to last bid");
        }
        
        // In case this is the first bid, jump over this
        if(item.lastBid.bidder != address(0)) _refundLastBid(item);
        
        // Update bid values
        item.lastBid.amount = msg.value;
        item.lastBid.bidder = msg.sender;

        emit BidRequest(
            _itemId,
            msg.sender,
            msg.value,
            block.timestamp
            );

        // In case bid is higher that buyout, proceed with buyout
        if(msg.value >= item.buyoutPrice) {
            _closeAuction(item);
        }

    }

    // Private utils

    function _refundLastBid(Item storage item) private returns(bool) {
        // Checks
        Bid memory previousBid = Bid(item.lastBid.bidder, item.lastBid.amount);        
        // Interactions
        (bool success,) = payable(item.lastBid.bidder).call{value: item.lastBid.amount}(""); // Full refund from last bid
        if(success){
            return success;
        } else {
            revert("Error transfering back last bid");
        }
    }


    function _closeAuction(Item storage item) private {
        // Update item status
        item.sold = true;
        
        // Transfer asset to final bidder
        uint fee = getFee(item.itemId);
        payable(item.seller).call{value:item.lastBid.amount - fee}("");
        payable(feeAccount).call{value: fee }("");
        item.nftContract.transferFrom(address(this), msg.sender, item.tokenId);
        emit ItemPurchased(
            _itemId,
            address(item.nftContract),
            item.tokenId,
            item.buyoutPrice,
            PurchaseType.HIGHEST_BID,
            item.seller,
            msg.sender,
            block.timestamp
            );
    }


    function _processBuyout(uint _itemId, uint _amount) private {
        Item storage item = items[_itemId];
        // Checks
        require(_itemId >= 0 && _itemId <= itemCount, "No such item listed");
        require(_amount >= item.buyoutPrice, "Not enough funds to cover for price and market fee");
        require(!item.sold, "Item not for sale anymore");  
        // Effects
        item.sold = true;      
        // Interactions
        uint fee = getFee(_itemId);
        payable(item.seller).call{value:item.buyoutPrice - fee}("");
        payable(feeAccount).call{value: fee }("");
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




    // View functions

    function getFee(uint _itemId) view public returns(uint) {
        return(items[_itemId].buyoutPrice*feePercentage/100);
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