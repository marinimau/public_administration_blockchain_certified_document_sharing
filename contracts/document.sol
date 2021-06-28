// contracts/document.sol
// SPDX-License-Identifier: CC-BY-4.0
/// @title PABCDS - PSAB2021
/// @author Mauro Marini


pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol"; 
import "@openzeppelin/contracts/utils/Counters.sol";


/**
 * @title Document
 * @dev Store & retrieve document version
 */
contract Document {

    documenr
    address documentAuthor;
    
    
    /**
     * @title DocumentVersion
     * @dev Struct for the document version
     */
    struct DocumentVersion {
        uint256 versionID;
        string documentURI;
        sha256 fingerPrint;
        address versionAuthor;
    }

    /**
     * @dev Store value in variable
     * @param num value to store
     */
    function store(uint256 num) public {
        number = num;
    }

    /**
     * @dev Return value 
     * @return value of 'number'
     */
    function retrieve() public view returns (uint256){
        return number;
    }
    
    
    modifier onlyDocumentAuthor(){
        require(author==msg.sender);
        _;
    }
    
    modifier onlyAuthorizedOperator(uint256 id){
        require(ownerOf(id)==msg.sender);
        _;
    }
}
