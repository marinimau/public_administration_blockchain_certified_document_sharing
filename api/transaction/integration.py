#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 05/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

import hashlib
from web3 import Web3, EthereumTesterProvider

from django.conf import settings
from .models import DocumentSC, DocumentVersionTransaction
from contracts.document_compiled import bytecode, abi


# ----------------------------------------------------------------------------------------------------------------------
#
#   Common
#
# ----------------------------------------------------------------------------------------------------------------------

def web3_connection(document_author):
    """
    Create the connection to the blockchain
    :param document_author: the document author
    :return: the connection
    """
    w3 = Web3(EthereumTesterProvider())
    # TODO: use infura and document author wallet
    assert (w3.isConnected())
    return w3


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document SC
#
# ----------------------------------------------------------------------------------------------------------------------

def deploy_contract(w3, document_page_url):
    """
    TDeploy the contract
    :param w3: the w3 connection
    :param document_page_url: the document page url
    :return: a pari tx_receipt, abi
    """
    print(type(abi))
    document_sc = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = document_sc.constructor(document_page_url).transact()
    return w3.eth.wait_for_transaction_receipt(tx_hash), abi


def create_document_contract(document):
    """
    Create a contract for a document obj
    :param document: the document obj
    :return:
    """
    # 1: create connection connection
    w3 = web3_connection(document.author)
    # 2: deploy contract
    document_page_url = str(settings.SITE_URL + str(document.id))
    tx_receipt, abi = deploy_contract(w3, document_page_url)
    # 3: store sc data
    DocumentSC.objects.create(transaction_address=tx_receipt.contractAddress,
                              author_address=document.author.bc_address, document=document)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version Transaction
#
# ----------------------------------------------------------------------------------------------------------------------

def calculate_hash_fingerprint(file_path):
    """
    Calculate the sha-256 fingerprint of the attached file
    :param file_path: the attached file path
    :return: the fingerprint
    """
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).digest()


def create_document_version_transaction(document_version):
    """
    Create a transaction for a document version obj
    :param document_version: the document_version obj
    :return:
    """
    # 1: create connection connection
    w3 = web3_connection(document_version.document.author)
    # 2: get the SC from document

    # 3: check if user can create transaction
    # 4: create the transaction in the SC
    document_version_page_url = str(settings.SITE_URL + 'version/' + str(document_version.id))
    fingerprint = calculate_hash_fingerprint(document_version.file_resource.path)
    tx_receipt = 0

    # 5: store transaction data
    '''
    DocumentVersionTransaction.objects.create(transaction_address=tx_receipt.contractAddress,
                                              author_address=document_version.author.bc_address,
                                              hash_fingerprint=fingerprint, document_version=document_version,
                                              download_url=document_version_page_url)
    '''
