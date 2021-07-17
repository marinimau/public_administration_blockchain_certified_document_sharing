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
        fingerprint = calculate_hash_fingerprint(self.documents_version.file_resource)
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
        self.assertEqual(result, '0xc53364bd323d7299a37f149d7391c10068aa02913645c4a86a4c8106838ae793')

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
