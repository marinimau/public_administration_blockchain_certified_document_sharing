#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 15/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#
from django.conf import settings
from web3 import Web3, EthereumTesterProvider
from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import to_wei
from django.test import TestCase

from api.transaction.utils.integration import deploy_contract, check_if_whitelisted, add_operator_to_whitelist, \
    remove_operator_from_whitelist
from contracts.document_compiled import abi

SECRET_KEY = '0x58d23b55bc9cdce1f18c2500f40ff4ab7245df9a89505e9b1fa4851f623d241d'


class SCTest(TestCase):
    """
    SC test acceptance class
    """

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Generic
    #
    # ------------------------------------------------------------------------------------------------------------------

    def setUp(self):
        """
        setup test data
        """
        self.init_test_connection()
        self.eth_tester = EthereumTester()
        # add account whit secret key
        state_overrides = {'balance': to_wei(100, 'ether')}
        PyEVMBackend._generate_genesis_state(overrides=state_overrides, num_accounts=3)
        self.auth_account = self.eth_tester.add_account(SECRET_KEY)
        # add other test accounts
        self.accounts = self.eth_tester.get_accounts()
        self.document_sc_address = self.document_sc_deploy()

    def init_test_connection(self):
        """
        init blockchain test connection
        """
        self.w3 = Web3(EthereumTesterProvider())

    def test_check_connection(self):
        """
        test the connection
        """
        self.assertTrue(self.w3.isConnected())

    def test_accounts(self):
        """
        check if the accounts are created
        """
        self.assertIsNotNone(self.accounts)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Document SC deploy
    #
    # ------------------------------------------------------------------------------------------------------------------

    def document_sc_deploy(self):
        """
        do the document sc deploy
        """
        return deploy_contract(self.w3, 'https://test-domain.com/1', SECRET_KEY)

    def test_document_sc_deploy(self):
        """
        test the document sc deploy
        """
        sc = self.document_sc_deploy()
        self.assertIsNotNone(sc)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Document transaction deploy
    #
    # ------------------------------------------------------------------------------------------------------------------

    def deploy_document_version(self, version_id=1):
        """
        deploy the document version
        :param: version_id: the id of the version
        """
        contract_receipt = self.document_sc_deploy()
        document_sc = self.w3.eth.contract(address=contract_receipt.contractAddress, abi=abi)
        if not check_if_whitelisted(document_sc, self.auth_account):
            add_operator_to_whitelist(self.w3, document_sc, SECRET_KEY, self.auth_account)
        # 4: get params
        # 5: create the transaction
        acct = self.w3.eth.account.from_key(SECRET_KEY)
        # 6. create the constructor transaction
        test_create_version_tx = document_sc.functions.createDocumentVersion(version_id, 'url',
                                                                             b'\xe0\x0eE%\xfa\xa9\x91\xb8"S\xc8ZF_'
                                                                             b'\x85\xe7\xdfm\xcb\x98X_v\xd9\t\xf4\x05'
                                                                             b'\x18vP\xdc\x03').buildTransaction(
            {
                'from': acct.address,
                'nonce': self.w3.eth.get_transaction_count(acct.address),
                'gas': settings.GAS_CONTRACT_DEPLOY,
                'gasPrice': 0
            })
        signed = acct.sign_transaction(test_create_version_tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.transactionHash.hex()

    def test_version_deploy(self):
        """
        Test the document version transaction
        """
        tx_address = self.deploy_document_version(version_id=2)
        tx = self.w3.eth.get_transaction(tx_address)
        self.assertIsNotNone(tx)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Whitelist management
    #
    # ------------------------------------------------------------------------------------------------------------------

    def test_add_to_whitelist(self):
        """
        Test add to whitelist
        """
        contract_receipt = self.document_sc_deploy()
        document_sc = self.w3.eth.contract(address=contract_receipt.contractAddress, abi=abi)
        # ensure that is removed
        remove_operator_from_whitelist(self.w3, document_sc, SECRET_KEY, self.auth_account)
        # add again
        add_operator_to_whitelist(self.w3, document_sc, SECRET_KEY, self.auth_account)
        whitelisted = check_if_whitelisted(document_sc, self.auth_account)
        # check that is in whitelsit
        self.assertTrue(whitelisted)

    def test_remove_from_whitelist(self):
        """
        Test remove from whitelist
        """
        contract_receipt = self.document_sc_deploy()
        document_sc = self.w3.eth.contract(address=contract_receipt.contractAddress, abi=abi)
        # ensure that is added
        add_operator_to_whitelist(self.w3, document_sc, SECRET_KEY, self.auth_account)
        # remove
        remove_operator_from_whitelist(self.w3, document_sc, SECRET_KEY, self.auth_account)
        whitelisted = check_if_whitelisted(document_sc, self.auth_account)
        # check that not is in whitelist
        self.assertFalse(whitelisted)
