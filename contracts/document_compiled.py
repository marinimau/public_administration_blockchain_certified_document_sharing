"""
This software is distributed under MIT/X11 license

Copyright (c) 2021 Mauro Marini - University of Cagliari

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import json

abi = json.loads(
    '''
            [
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "_documentURI",
                        "type": "string"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "account",
                        "type": "address"
                    }
                ],
                "name": "AddedToWhitelist",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "previousOwner",
                        "type": "address"
                    },
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "newOwner",
                        "type": "address"
                    }
                ],
                "name": "OwnershipTransferred",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "account",
                        "type": "address"
                    }
                ],
                "name": "RemovedFromWhitelist",
                "type": "event"
            },
            {
                "inputs": [
                    {
                        "internalType": "address[]",
                        "name": "addrs",
                        "type": "address[]"
                    }
                ],
                "name": "addAddressesToWhitelist",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "_address",
                        "type": "address"
                    }
                ],
                "name": "addToWhiteList",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_documentVersionID",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "_documentVersionURI",
                        "type": "string"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "_fingerPrint",
                        "type": "bytes32"
                    }
                ],
                "name": "createDocumentVersion",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "_address",
                        "type": "address"
                    }
                ],
                "name": "isWhitelisted",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "owner",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address[]",
                        "name": "addrs",
                        "type": "address[]"
                    }
                ],
                "name": "removeAddressesFromWhitelist",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "_address",
                        "type": "address"
                    }
                ],
                "name": "removeFromWhiteList",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "renounceOwnership",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "retrieveDocumentAuthor",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "retrieveDocumentURI",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_documentVersionID",
                        "type": "uint256"
                    }
                ],
                "name": "retrieveDocumentVersion",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "documentVersionID",
                                "type": "uint256"
                            },
                            {
                                "internalType": "string",
                                "name": "documentVersionURI",
                                "type": "string"
                            },
                            {
                                "internalType": "bytes32",
                                "name": "fingerPrint",
                                "type": "bytes32"
                            },
                            {
                                "internalType": "address",
                                "name": "versionAuthor",
                                "type": "address"
                            }
                        ],
                        "internalType": "struct Document.DocumentVersion",
                        "name": "version",
                        "type": "tuple"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "newOwner",
                        "type": "address"
                    }
                ],
                "name": "transferOwnership",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "name": "versions",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "documentVersionID",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "documentVersionURI",
                        "type": "string"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "fingerPrint",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "address",
                        "name": "versionAuthor",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    '''
)

bytecode = "60806040523480156200001157600080fd5b5060405162001a3f38038062001a3f833981810160405281019062000037919062000265565b620000576200004b6200007760201b60201c565b6200007f60201b60201c565b80600190805190602001906200006f92919062000143565b50506200041a565b600033905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050816000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a35050565b82805462000151906200033f565b90600052602060002090601f016020900481019282620001755760008555620001c1565b82601f106200019057805160ff1916838001178555620001c1565b82800160010185558215620001c1579182015b82811115620001c0578251825591602001919060010190620001a3565b5b509050620001d09190620001d4565b5090565b5b80821115620001ef576000816000905550600101620001d5565b5090565b60006200020a6200020484620002d3565b620002aa565b9050828152602081018484840111156200022357600080fd5b6200023084828562000309565b509392505050565b600082601f8301126200024a57600080fd5b81516200025c848260208601620001f3565b91505092915050565b6000602082840312156200027857600080fd5b600082015167ffffffffffffffff8111156200029357600080fd5b620002a18482850162000238565b91505092915050565b6000620002b6620002c9565b9050620002c4828262000375565b919050565b6000604051905090565b600067ffffffffffffffff821115620002f157620002f0620003da565b5b620002fc8262000409565b9050602081019050919050565b60005b83811015620003295780820151818401526020810190506200030c565b8381111562000339576000848401525b50505050565b600060028204905060018216806200035857607f821691505b602082108114156200036f576200036e620003ab565b5b50919050565b620003808262000409565b810181811067ffffffffffffffff82111715620003a257620003a1620003da565b5b80604052505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f8301169050919050565b611615806200042a6000396000f3fe608060405234801561001057600080fd5b50600436106100cf5760003560e01c806387aee00e1161008c5780639629452d116100665780639629452d14610201578063cc712feb1461021d578063e2ec6ec31461023b578063f2fde38b14610257576100cf565b806387aee00e14610180578063882ff2c6146101b35780638da5cb5b146101e3576100cf565b806301bf6648146100d45780630e7e7c01146100f057806324953eaa1461010e5780633af32abf1461012a57806347ee03941461015a578063715018a614610176575b600080fd5b6100ee60048036038101906100e99190610f11565b610273565b005b6100f861038d565b60405161010591906111c5565b60405180910390f35b61012860048036038101906101239190610f3a565b61041f565b005b610144600480360381019061013f9190610f11565b610507565b60405161015191906111aa565b60405180910390f35b610174600480360381019061016f9190610f11565b61055d565b005b61017e610677565b005b61019a60048036038101906101959190610f7b565b6106ff565b6040516101aa9493929190611249565b60405180910390f35b6101cd60048036038101906101c89190610f7b565b6107d7565b6040516101da9190611227565b60405180910390f35b6101eb610930565b6040516101f8919061118f565b60405180910390f35b61021b60048036038101906102169190610fa4565b610959565b005b610225610a35565b604051610232919061118f565b60405180910390f35b61025560048036038101906102509190610f3a565b610a44565b005b610271600480360381019061026c9190610f11565b610b2c565b005b61027b610c24565b73ffffffffffffffffffffffffffffffffffffffff16610299610930565b73ffffffffffffffffffffffffffffffffffffffff16146102ef576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016102e690611207565b60405180910390fd5b6000600360008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508073ffffffffffffffffffffffffffffffffffffffff167fcdd2e9b91a56913d370075169cefa1602ba36be5301664f752192bb1709df75760405160405180910390a250565b60606001805461039c906113d8565b80601f01602080910402602001604051908101604052809291908181526020018280546103c8906113d8565b80156104155780601f106103ea57610100808354040283529160200191610415565b820191906000526020600020905b8154815290600101906020018083116103f857829003601f168201915b5050505050905090565b610427610c24565b73ffffffffffffffffffffffffffffffffffffffff16610445610930565b73ffffffffffffffffffffffffffffffffffffffff161461049b576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161049290611207565b60405180910390fd5b60005b8151811015610503576104f08282815181106104e3577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b6020026020010151610273565b80806104fb9061143b565b91505061049e565b5050565b6000600360008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff169050919050565b610565610c24565b73ffffffffffffffffffffffffffffffffffffffff16610583610930565b73ffffffffffffffffffffffffffffffffffffffff16146105d9576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105d090611207565b60405180910390fd5b6001600360008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508073ffffffffffffffffffffffffffffffffffffffff167fa850ae9193f515cbae8d35e8925bd2be26627fc91bce650b8652ed254e9cab0360405160405180910390a250565b61067f610c24565b73ffffffffffffffffffffffffffffffffffffffff1661069d610930565b73ffffffffffffffffffffffffffffffffffffffff16146106f3576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016106ea90611207565b60405180910390fd5b6106fd6000610c2c565b565b6002602052806000526040600020600091509050806000015490806001018054610728906113d8565b80601f0160208091040260200160405190810160405280929190818152602001828054610754906113d8565b80156107a15780601f10610776576101008083540402835291602001916107a1565b820191906000526020600020905b81548152906001019060200180831161078457829003601f168201915b5050505050908060020154908060030160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905084565b6107df610cf0565b6000600260008481526020019081526020016000206001018054610802906113d8565b90501461092a576002600083815260200190815260200160002060405180608001604052908160008201548152602001600182018054610841906113d8565b80601f016020809104026020016040519081016040528092919081815260200182805461086d906113d8565b80156108ba5780601f1061088f576101008083540402835291602001916108ba565b820191906000526020600020905b81548152906001019060200180831161089d57829003601f168201915b50505050508152602001600282015481526020016003820160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681525050905061092b565b5b919050565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b61096233610507565b61096b57600080fd5b60405180608001604052808481526020018381526020018281526020013373ffffffffffffffffffffffffffffffffffffffff16815250600260008581526020019081526020016000206000820151816000015560208201518160010190805190602001906109db929190610d31565b506040820151816002015560608201518160030160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550905050505050565b6000610a3f610930565b905090565b610a4c610c24565b73ffffffffffffffffffffffffffffffffffffffff16610a6a610930565b73ffffffffffffffffffffffffffffffffffffffff1614610ac0576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610ab790611207565b60405180910390fd5b60005b8151811015610b2857610b15828281518110610b08577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b602002602001015161055d565b8080610b209061143b565b915050610ac3565b5050565b610b34610c24565b73ffffffffffffffffffffffffffffffffffffffff16610b52610930565b73ffffffffffffffffffffffffffffffffffffffff1614610ba8576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610b9f90611207565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff161415610c18576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610c0f906111e7565b60405180910390fd5b610c2181610c2c565b50565b600033905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050816000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a35050565b6040518060800160405280600081526020016060815260200160008019168152602001600073ffffffffffffffffffffffffffffffffffffffff1681525090565b828054610d3d906113d8565b90600052602060002090601f016020900481019282610d5f5760008555610da6565b82601f10610d7857805160ff1916838001178555610da6565b82800160010185558215610da6579182015b82811115610da5578251825591602001919060010190610d8a565b5b509050610db39190610db7565b5090565b5b80821115610dd0576000816000905550600101610db8565b5090565b6000610de7610de2846112ba565b611295565b90508083825260208201905082856020860282011115610e0657600080fd5b60005b85811015610e365781610e1c8882610e7e565b845260208401935060208301925050600181019050610e09565b5050509392505050565b6000610e53610e4e846112e6565b611295565b905082815260208101848484011115610e6b57600080fd5b610e76848285611396565b509392505050565b600081359050610e8d8161159a565b92915050565b600082601f830112610ea457600080fd5b8135610eb4848260208601610dd4565b91505092915050565b600081359050610ecc816115b1565b92915050565b600082601f830112610ee357600080fd5b8135610ef3848260208601610e40565b91505092915050565b600081359050610f0b816115c8565b92915050565b600060208284031215610f2357600080fd5b6000610f3184828501610e7e565b91505092915050565b600060208284031215610f4c57600080fd5b600082013567ffffffffffffffff811115610f6657600080fd5b610f7284828501610e93565b91505092915050565b600060208284031215610f8d57600080fd5b6000610f9b84828501610efc565b91505092915050565b600080600060608486031215610fb957600080fd5b6000610fc786828701610efc565b935050602084013567ffffffffffffffff811115610fe457600080fd5b610ff086828701610ed2565b925050604061100186828701610ebd565b9150509250925092565b61101481611344565b82525050565b61102381611344565b82525050565b61103281611356565b82525050565b61104181611362565b82525050565b61105081611362565b82525050565b600061106182611317565b61106b8185611322565b935061107b8185602086016113a5565b61108481611511565b840191505092915050565b600061109a82611317565b6110a48185611333565b93506110b48185602086016113a5565b6110bd81611511565b840191505092915050565b60006110d5602683611333565b91506110e082611522565b604082019050919050565b60006110f8602083611333565b915061110382611571565b602082019050919050565b60006080830160008301516111266000860182611171565b506020830151848203602086015261113e8282611056565b91505060408301516111536040860182611038565b506060830151611166606086018261100b565b508091505092915050565b61117a8161138c565b82525050565b6111898161138c565b82525050565b60006020820190506111a4600083018461101a565b92915050565b60006020820190506111bf6000830184611029565b92915050565b600060208201905081810360008301526111df818461108f565b905092915050565b60006020820190508181036000830152611200816110c8565b9050919050565b60006020820190508181036000830152611220816110eb565b9050919050565b60006020820190508181036000830152611241818461110e565b905092915050565b600060808201905061125e6000830187611180565b8181036020830152611270818661108f565b905061127f6040830185611047565b61128c606083018461101a565b95945050505050565b600061129f6112b0565b90506112ab828261140a565b919050565b6000604051905090565b600067ffffffffffffffff8211156112d5576112d46114e2565b5b602082029050602081019050919050565b600067ffffffffffffffff821115611301576113006114e2565b5b61130a82611511565b9050602081019050919050565b600081519050919050565b600082825260208201905092915050565b600082825260208201905092915050565b600061134f8261136c565b9050919050565b60008115159050919050565b6000819050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b82818337600083830152505050565b60005b838110156113c35780820151818401526020810190506113a8565b838111156113d2576000848401525b50505050565b600060028204905060018216806113f057607f821691505b60208210811415611404576114036114b3565b5b50919050565b61141382611511565b810181811067ffffffffffffffff82111715611432576114316114e2565b5b80604052505050565b60006114468261138c565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82141561147957611478611484565b5b600182019050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f8301169050919050565b7f4f776e61626c653a206e6577206f776e657220697320746865207a65726f206160008201527f6464726573730000000000000000000000000000000000000000000000000000602082015250565b7f4f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572600082015250565b6115a381611344565b81146115ae57600080fd5b50565b6115ba81611362565b81146115c557600080fd5b50565b6115d18161138c565b81146115dc57600080fd5b5056fea26469706673582212205e5e079ac22fffa9af9dced0f1f73ad23dfba61dde8553180eec42200638fcbb64736f6c63430008040033"
