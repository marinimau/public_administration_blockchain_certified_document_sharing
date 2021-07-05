#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 05/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from web3 import Web3
from solcx import compile_source

from django.conf import settings
from .models import DocumentSC, DocumentVersionTransaction


def web3_connection(document_author):
    """
    Create the connection to the blockchain
    :param document_author: the document author
    :return: the connection
    """
    w3 = Web3(Web3.EthereumTesterProvider())
    w3.eth.default_account = w3.eth.accounts[0]
    # TODO: use infura and document author wallet
    assert(w3.isConnected())
    return w3


def compile_contract():
    """
    Compile the contract from source code
    :return: the contract bytecode
    """
    with open('../../contracts/document.sol', 'r') as file:
        data = file.read().replace('\n', '')
    return compile_source(data)


def deploy_contract(w3, compiled_contract, document_page_url):
    """
    TDeploy the contract
    :param w3: the w3 connection
    :param compiled_contract: the compiled contract
    :param document_page_url: the document page url
    :return:
    """
    contract_id, contract_interface = compiled_contract.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']
    document_sc = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = document_sc.constructor().transact()
    return w3.eth.wait_for_transaction_receipt(tx_hash)


def create_document_contract(document):
    """
    Create a contract for a document obj
    :param document: the document obj
    :return:
    """
    # 1: create connection connection
    w3 = web3_connection(document.author)
    # 2: compile contract from source code
    compiled_contract = compile_contract()
    # 3: deploy contract
    document_page_url = str(settings.SITE_URL + str(document.id))
    tx_receipt = deploy_contract(w3, compiled_contract, document_page_url)
    # 4: store transaction data
    # DocumentSC.objects.create()





