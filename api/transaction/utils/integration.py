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

import hashlib
import sys
from pathlib import Path

from rest_framework import serializers
from web3 import Web3, HTTPProvider

from django.conf import settings
from api.transaction.models import DocumentSC, DocumentVersionTransaction
from contents.messages.get_messages import get_transaction_messages
from contracts.document_compiled import bytecode, abi

transaction_messages = get_transaction_messages()


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
    w3 = Web3(HTTPProvider(settings.HTTP_PROVIDER_URL))
    assert (w3.isConnected())
    return w3


def get_gas_price(w3):
    """
    return the gas price
    :param w3: the w3 connection
    """
    if 'test' not in sys.argv:
        return settings.GAS_PRICE
    return 0


def check_balance(w3, address, minimum_required=settings.GAS_CONTRACT_DEPLOY):
    """
    Check if the operator has enough Wei in their balance
    :param w3: the w3 connection
    :param address: the operator address
    :param minimum_required: the minim wei required
    :return:
    """
    balance = w3.eth.get_balance(address)
    if balance is not None and balance < minimum_required:
        raise serializers.ValidationError(transaction_messages['balance_is_to_low'])


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
    gas_required = settings.GAS_CONTRACT_DEPLOY
    gas_price = get_gas_price(w3)
    acct = w3.eth.account.from_key(secret_key)
    check_balance(w3, acct.address, minimum_required=(gas_required * gas_price))
    # 3. create the constructor transaction
    construct_txn = document_sc.constructor(document_page_url).buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.get_transaction_count(acct.address),
        'gas': gas_required,
        'gasPrice': gas_price})
    # 4. sign transaction
    signed = acct.sign_transaction(construct_txn)
    # 5. send signed transaction
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
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

def calculate_hash_fingerprint(file):
    """
    Calculate the sha-256 fingerprint of the attached file
    :param file: the attached file
    :return: the fingerprint
    """
    if file is not None and Path(file.path).exists():
        file.open(mode='rb')
        digest = hashlib.sha256(file.read()).digest()
        file.close()
        return digest
    return hashlib.sha256().digest()


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


def create_document_version_transaction(document_version, w3=None):
    """
    Create a transaction for a document version obj
    :param document_version: the document_version obj
    :param w3: the w3 connection
    :return:
    """
    # 1: create connection connection
    if w3 is None:
        w3 = web3_connection()
    # 2: get the SC from document
    sc = get_contract(w3, document_version.document.id)
    if sc is not None:
        # 3: check if user can create transaction
        if not check_if_whitelisted(sc, document_version.author.bc_address):
            add_operator_to_whitelist(w3, sc, document_version.document.author.bc_secret_key,
                                      document_version.author.bc_address)
        # 4: get params
        document_version_page_url = str(settings.SITE_URL + 'version/' + str(document_version.id))
        fingerprint = calculate_hash_fingerprint(document_version.file_resource)
        # 5: create the transaction
        acct = w3.eth.account.from_key(document_version.document.author.bc_secret_key)
        gas_required = settings.GAS_NEW_VERSION_TRANSACTION
        gas_price = get_gas_price(w3)
        check_balance(w3, acct.address, minimum_required=(gas_required * gas_price))
        # 6. create the constructor transaction
        create_version_tx = sc.functions.createDocumentVersion(document_version.id, document_version_page_url,
                                                               fingerprint).buildTransaction({
            'from': acct.address,
            'nonce': w3.eth.get_transaction_count(acct.address),
            'gas': gas_required,
            'gasPrice': gas_price})
        # 7. sign transaction
        signed = acct.sign_transaction(create_version_tx)
        # 8. send signed transaction
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        transaction_address = tx_receipt.transactionHash.hex()
        # 9: store transaction data
        DocumentVersionTransaction.objects.create(transaction_address=transaction_address,
                                                  author_address=document_version.author.bc_address,
                                                  hash_fingerprint=fingerprint, document_version=document_version,
                                                  download_url=document_version_page_url)
    else:
        raise serializers.ValidationError(transaction_messages['sc_not_found'])


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document version validation
#
# ----------------------------------------------------------------------------------------------------------------------

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
        if len(output) == 4:
            bc_fingerprint = output[2]
            local_fingerprint = calculate_hash_fingerprint(document_version.file_resource)
            result = 1 if bc_fingerprint == local_fingerprint else -1
            return result, transaction_address
    return 0, None


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
    return sc.functions.isWhitelisted(operator_address).call()


def add_operator_to_whitelist(w3, sc, owner_secret_key, operator_address):
    """
    Add an operator to the whitelist
    :param w3: the w3 connection
    :param owner_secret_key: the secret key of the document owner
    :param sc: the document sc
    :param operator_address: the operator address to add
    :return:
    """
    acct = w3.eth.account.from_key(owner_secret_key)
    gas_required = settings.GAS_ADD_REMOVE_WHITELIST
    gas_price = get_gas_price(w3)
    check_balance(w3, acct.address, minimum_required=(gas_required * gas_price))
    # 2. build transaction
    add_to_whitelist_tx = sc.functions.addToWhiteList(operator_address).buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.get_transaction_count(acct.address),
        'gas': gas_required,
        'gasPrice': gas_price})
    # 3. sign transaction
    signed = acct.sign_transaction(add_to_whitelist_tx)
    # 4. send signed transaction
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)


def remove_operator_from_whitelist(w3, sc, owner_secret_key, operator_address):
    """
    Remove an operator from the whitelist
    :param w3: the w3 connection
    :param owner_secret_key: the secret key of the document owner
    :param sc: the document sc
    :param operator_address: the operator address to remove
    :return:
    """
    gas_required = settings.GAS_ADD_REMOVE_WHITELIST
    gas_price = get_gas_price(w3)
    acct = w3.eth.account.from_key(owner_secret_key)
    check_balance(w3, acct.address, minimum_required=(gas_required * gas_price))
    # 2. build transaction
    remove_from_whitelist_tx = sc.functions.removeFromWhiteList(operator_address).buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.get_transaction_count(acct.address),
        'gas': gas_required,
        'gasPrice': gas_price})
    # 3. sign transaction
    signed = acct.sign_transaction(remove_from_whitelist_tx)
    # 4. send signed transaction
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
