#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 15/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from web3 import Web3, EthereumTesterProvider
from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import to_wei
from django.test import TestCase

from api.transaction.utils.integration import deploy_contract

SECRET_KEY = '0x58d23b55bc9cdce1f18c2500f40ff4ab7245df9a89505e9b1fa4851f623d241d'


class SCTest(TestCase, ):
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
        self.document_sc = self.document_sc_deploy()

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

    def deploy_document_version(self):
        """
        deploy the document version
        """
        pass