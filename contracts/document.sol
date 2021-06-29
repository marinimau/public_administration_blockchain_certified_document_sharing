// contracts/document.sol
// SPDX-License-Identifier: CC-BY-4.0
/// @title PABCDS - PSAB2021
/// @author Mauro Marini


pragma solidity ^0.8.0;


import "@openzeppelin/contracts/access/Ownable.sol"; 


/**
 * @title Document
 * @dev Store & retrieve document version, versions can be created nlòy by white listed operators
 */
contract Document is Ownable{

    string documentURI;
    address documentAuthor;
    mapping(uint256 => DocumentVersion) public versions;
    mapping(address => bool) whitelist;
    
    
    event AddedToWhitelist(address indexed account);
    event RemovedFromWhitelist(address indexed account);
    
    
    /**
     * @title DocumentVersion
     * @dev Struct for the document version
     */
    struct DocumentVersion {
        uint256 documentVersionID;
        string documentVersionURI;
        bytes32 fingerPrint;
        address versionAuthor;
    }

    /**
     * @dev Store create a document
     * @param _documentURI the URI of the document page in the centralized app
     */
    constructor(string memory _documentURI) {
        documentURI = _documentURI;
        documentAuthor == msg.sender;
    }
    
    
    /**
     * --------------------------------------------------------
     * View
     * --------------------------------------------------------
     */

    /**
     * @dev Return value of the documentURI
     * @return value of 'documentURI'
     */
    function retrieveDocumentURI() public view returns (string memory){
        return documentURI;
    }
    
    /**
     * @dev Return address of the author of the document
     * @return value of 'documentAuthor'
     */
    function retrieveDocumentAuthor() public view returns (address){
        return documentAuthor;
    }
    
     /**
     * @dev Retrieve a version of the document
     * @param _documentVersionID: the id of the version
     */
    function retrieveDocumentVersion(uint256 _documentVersionID) public view returns (DocumentVersion memory version) {
        if (bytes(versions[_documentVersionID].documentVersionURI).length != 0) {
            return versions[_documentVersionID];
        }
    }
    
    /**
     * --------------------------------------------------------
     * Version creation
     * --------------------------------------------------------
     */
    
    /**
     * @dev Create a version for the document
     * @param _documentVersionID: the id of the version
     * @param _documentVersionURI: the URI of the document version in the centralized app
     * @param _fingerPrint: the sha256 fingerPrint of the version attached file.
     */
    function createDocumentVersion(uint256 _documentVersionID, string memory _documentVersionURI, bytes32 _fingerPrint) public onlyWhitelisted{
        versions[_documentVersionID] = DocumentVersion(_documentVersionID, _documentVersionURI, _fingerPrint, msg.sender);
    }
    
    
    /**
     * --------------------------------------------------------
     * WhiteList
     * --------------------------------------------------------
     */
    
    /**
     * @dev Add an operator to whitelist
     * @param _address the address of the operator
     */
    function addToWhiteList(address _address) public onlyOwner {
        whitelist[_address] = true;
        emit AddedToWhitelist(_address);
    }

     /**
     * @dev Remove an operator to whitelist
     * @param _address the address of the operator
     */
    function removeFromWhiteList(address _address) public onlyOwner {
        whitelist[_address] = false;
        emit RemovedFromWhitelist(_address);
    }

     /**
     * @dev Check if an operator is in whitelist
     * @param _address the address of the operator
     * @return a flag that indicates if the operator is in the whitelist
     */
    function isWhitelisted(address _address) public view returns(bool) {
        return whitelist[_address];
    }
    
    
    /**
     * --------------------------------------------------------
     * Modifiers
     * --------------------------------------------------------
     */

    /**
     * requires that the sender is inside the whitelist
     */
    modifier onlyWhitelisted() {
        require(isWhitelisted(msg.sender));
        _;
    }

    
}
