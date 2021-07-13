#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 10/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.test import TestCase
from rest_framework import serializers

from api.document.models import DocumentVersion
from api.transaction.test.abstract_transaction_test import TransactionTestAbstract
from api.transaction.utils.integration import calculate_hash_fingerprint
from api.transaction.utils.view_utils import validate_version_id


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
        calculate fingerprint
        """
        fingerprint = calculate_hash_fingerprint(self.file)
        self.assertEqual(fingerprint,
                         b'\xe0\xac6\x01\x00]\xfa\x18d\xf59*\xab\xaf}\x89\x8b\x1b['
                         b'\xab\x85O\x1a\xcbD\x91\xbc\xd8\x06\xb7k\x0c')

