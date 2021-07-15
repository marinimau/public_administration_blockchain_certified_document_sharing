#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 10/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from api.transaction.test.abstract_transaction_test import TransactionTestAbstract
from api.transaction.utils.integration import calculate_hash_fingerprint
from api.transaction.utils.view_utils import validate_version_id
from ..utils.integration import get_contract, get_transaction, web3_connection, check_if_whitelisted
from contracts.document_compiled import abi


class TransactionTestUnit(TransactionTestAbstract):
    """
    Transaction unit test class
    """

    def test_validate_version_id(self):
        """
        validate version id test (valid document version)
        """
        result = validate_version_id(self.documents_version.id)
        self.assertTrue(isinstance(result, int))

    def test_calculate_fingerprint(self):
        """
        calculate fingerprint (ok)
        """
        fingerprint = calculate_hash_fingerprint(self.file)
        self.assertEqual(fingerprint,
                         b'\xe0\x0eE%\xfa\xa9\x91\xb8"S\xc8ZF_\x85\xe7\xdfm\xcb\x98X_v\xd9\t\xf4\x05\x18vP\xdc\x03')

    def test_get_contract(self):
        """
        Get document sc test (ok)
        """
        w3 = web3_connection()
        result = get_contract(w3, self.document.id)
        self.assertEqual(str(type(result)), "<class 'web3._utils.datatypes.Contract'>")

    def test_get_contract_fail(self):
        """
        Get document sc test (fail)
        """
        w3 = web3_connection()
        result = get_contract(w3, self.document2.id + 1)
        self.assertEqual(result, None)

    def test_get_version_transaction(self):
        """
        Get document version transaction test (ok)
        """
        result = get_transaction(self.documents_version.id)
        self.assertEqual(result, '0x02cd10878c32bb26c19feb3dcf414fac060b8acddd9ff0cac4ead45d7425b9e2')

    def test_get_version_transaction_fail(self):
        """
        Get document version transaction test (fail)
        """
        result = get_transaction(self.documents_version2.id + 1)
        self.assertEqual(result, None)

    def test_check_if_whitelisted(self):
        """
        Check if whitelisted test (true)
        """
        w3 = web3_connection()
        sc_address = '0x65138ba4ea251D8E96DB11cEad9285EE66039157'
        sc = w3.eth.contract(address=sc_address, abi=abi)
        whitelisted = check_if_whitelisted(sc, self.operator.bc_address)
        self.assertTrue(whitelisted)

    def test_check_if_whitelisted_fail(self):
        """
        Check if whitelisted test (true)
        """
        w3 = web3_connection()
        sc_address = '0x65138ba4ea251D8E96DB11cEad9285EE66039157'
        sc = w3.eth.contract(address=sc_address, abi=abi)
        whitelisted = check_if_whitelisted(sc, self.operator2.bc_address)
        self.assertFalse(whitelisted)
