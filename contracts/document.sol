// contracts/document.sol
// SPDX-License-Identifier: CC-BY-4.0
/// @title PABCDS - PSAB2021
/// @author Mauro Marini


pragma solidity ^0.8.0;



/**
 * @title Document
 * @dev Store & retrieve document version
 */
contract Document{

    string documentURI;
    address documentAuthor;
    mapping(uint256 => DocumentVersion) private versions;
    
    
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
     * @dev Create a version for the document
     * @param documentVersionID: the id of the version
     * @param documentVersionURI: the URI of the document version in the centralized app
     * @param fingerPrint: the sha256 fingerPrint of the version attached file.
     */
    function createDocumentVersion(uint256 documentVersionID, string memory documentVersionURI, bytes32 fingerPrint) public {
        versions[documentVersionID] = DocumentVersion(documentVersionID, documentVersionURI, fingerPrint, msg.sender);
    }
    
    
    modifier onlyDocumentAuthor(){
        require(documentAuthor==msg.sender);
        _;
    }
    
}
