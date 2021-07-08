#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 05/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

import hashlib
from web3 import Web3, HTTPProvider, EthereumTesterProvider

from django.conf import settings
from api.transaction.models import DocumentSC, DocumentVersionTransaction
from contracts.document_compiled import bytecode, abi
from .network_params import *


# ----------------------------------------------------------------------------------------------------------------------
#
#   Common
#
# ----------------------------------------------------------------------------------------------------------------------

def web3_connection():
    """
    Create the connection to the blockchain
    :return: the connection
    """
    w3 = Web3(HTTPProvider(HTTP_PROVIDER_URL))
    assert (w3.isConnected())
    return w3


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document SC
#
# ----------------------------------------------------------------------------------------------------------------------

def deploy_contract(w3, document_page_url, secret_key):
    """
    TDeploy the contract
    :param w3: the w3 connection
    :param document_page_url: the document page url
    :param secret_key: the operator secret key
    :return: a pari tx_receipt, abi
    """
    # 1. declare contract
    document_sc = w3.eth.contract(abi=abi, bytecode=bytecode)
    # 2. authenticate operator
    acct = w3.eth.account.privateKeyToAccount(secret_key)
    print(acct.address)
    # 3. create the constructor transaction
    construct_txn = document_sc.constructor(document_page_url).buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': GAS_CONTRACT_DEPLOY,
        'gasPrice': GAS_PRICE})
    # 4. sign transaction
    signed = acct.signTransaction(construct_txn)
    # 5. send signed transaction
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)


def create_document_contract(document):
    """
    Create a contract for a document obj
    :param document: the document obj
    :return:
    """
    # 1: create connection connection
    w3 = web3_connection()
    # 2: deploy contract
    document_page_url = str(settings.SITE_URL + str(document.id))
    secret_key = document.author.bc_secret_key
    tx_receipt = deploy_contract(w3, document_page_url, secret_key)
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


def get_contract(w3, document_id):
    """
    Get the sc linked to the document
    :param w3: the web3 instance
    :param document_id: the id of the document
    :return: the contract or None
    """
    if DocumentSC.objects.filter(document__id=document_id).exists():
        contract_address = DocumentSC.objects.get(document__id=document_id).transaction_address
        return w3.eth.contract(address=contract_address, abi=abi)
    return None


def create_document_version_transaction(document_version):
    """
    Create a transaction for a document version obj
    :param document_version: the document_version obj
    :return:
    """
    # 1: create connection connection
    w3 = web3_connection()
    # 2: get the SC from document
    sc = get_contract(w3, document_version.document.id)
    if sc is not None:
        # 3: check if user can create transaction
        if not check_if_whitelisted(sc, document_version.author.bc_address):
            add_operator_to_whitelist(sc, document_version.author.bc_address)
        # 4: create the transaction in the SC
        document_version_page_url = str(settings.SITE_URL + 'version/' + str(document_version.id))
        fingerprint = calculate_hash_fingerprint(document_version.file_resource.path)
        tx_hash = sc.functions.createDocumentVersion(document_version.id, document_version_page_url,
                                                     fingerprint).transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        transaction_address = tx_receipt.transactionHash.hex()
        # 5: store transaction data
        DocumentVersionTransaction.objects.create(transaction_address=transaction_address,
                                                  author_address=document_version.author.bc_address,
                                                  hash_fingerprint=fingerprint, document_version=document_version,
                                                  download_url=document_version_page_url)


def get_transaction(document_version_id):
    """
    Get the transaction linked to the document version
    :param document_version_id: the id of the document version
    :return: the DocumentVersionTransaction address or None
    """
    if DocumentVersionTransaction.objects.filter(document_version__id=document_version_id).exists():
        return DocumentVersionTransaction.objects.get(document_version__id=document_version_id).transaction_address
    return None


def validate_document_version(document_version):
    """
    Given a document version check if bc stored fingerpint is equal to ready-to-download resource fingerprint
    :param document_version: the document version obj
    :return: a valid fingerpint flag (int)
    """
    w3 = web3_connection()
    # 1. check if exists transaction for the given document version
    transaction_address = get_transaction(document_version.id)
    sc = get_contract(w3, document_version.document.id)
    if sc is not None and transaction_address is not None:
        # 2. get transaction from blockchain
        output = sc.functions.retrieveDocumentVersion(document_version.id).call()
        print(output)
        return 1, None
    return 0, None  # PENDING


# ----------------------------------------------------------------------------------------------------------------------
#
#   Whitelist management
#
# ----------------------------------------------------------------------------------------------------------------------

def check_if_whitelisted(sc, operator_address):
    """
    Check if the operator can perform version creation
    :param sc: the document sc
    :param operator_address: the operator address
    :return: a flag that indicates if is whitelisted
    """
    return False


def add_operator_to_whitelist(sc, operator_address):
    """
    Add an operator to the whitelist
    :param sc: the document sc
    :param operator_address: the operator address
    :return:
    """
    pass


def remove_operator_from_whitelist(sc, operator_address):
    """
    Remove an operator from the whitelist
    :param sc: the document sc
    :param operator_address: the operator address
    :return:
    """
    pass
