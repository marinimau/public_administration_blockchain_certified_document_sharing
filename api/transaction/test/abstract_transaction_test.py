#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 10/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework.test import APITestCase

from ..models import DocumentVersionTransaction


class TransactionTestAbstract(APITestCase):
    """
    Test for transaction app
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set-up the data for the test
        :return:
        """
        cls.valid_transaction = DocumentVersionTransaction.objects.create(
            author_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            transaction_address='0xacfa697d0aa65d1a8f533f198ac0499ee866d9bf24240a99bd67e10cee6ff6c0',
            hash_fingerprint=b'U\xef7>X\xc4\xd3\x08\x96zE\xf3 \xe7\x95\x85\xd5\xdd\x829\xabu"f\xb8Bl\xdb\x12v\xa7\x98',
            download_url='https://siteurl.com/version/57'
        )
        cls.invalid_transaction = DocumentVersionTransaction.objects.create(
            author_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            transaction_address='0xacfa697d0aa65d1a8f533f198ac0499ee866d9bf24240a99bd67e10cee6ff6c0',
            hash_fingerprint=b"|C\xca~\x0cbm'\x10\xf6:\x93)\xd5\xd0P\xbf\x8bRP\xc8Q\xc3|\xf6\xf1q\xe2S\x96\xdb\xc9",
            download_url='https://siteurl.com/version/57'
        )

