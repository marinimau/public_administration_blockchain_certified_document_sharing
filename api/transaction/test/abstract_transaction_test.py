#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 10/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from ..models import DocumentVersionTransaction, DocumentSC
from ...document.models import Document, DocumentVersion
from ...user.models import PublicAuthority, PaOperator


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
        # 1. setup pa
        cls.public_authority = PublicAuthority.objects.create(name='test')
        # 2. setup author
        cls.operator = PaOperator.objects.create(
            username='operator',
            email='operator@operators.com',
            password='test',
            is_active=True,
            operator_code='OP1',
            public_authority=cls.public_authority,
            bc_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            bc_secret_key='secret'
        )
        cls.operator2 = PaOperator.objects.create(
            username='operator2',
            email='operator2@operators.com',
            password='test',
            is_active=True,
            operator_code='OP2',
            public_authority=cls.public_authority,
            bc_address='0x9737d773D02cdeC489BD86354188676688A29972',
            bc_secret_key='secret'
        )
        cls.operator.set_password('PaOperator123.')
        # 3. setup Document
        cls.document = Document.objects.create(
            title='Document',
            description='This is the description of the document ',
            author=cls.operator,
            require_permission=True
        )
        cls.document2 = Document.objects.create(
            title='Document',
            description='This is the description of the document ',
            author=cls.operator,
            require_permission=True
        )
        # 4. setup Document Version
        cls.file = SimpleUploadedFile(
            "file.txt",
            b"file content"
        )
        cls.documents_version = DocumentVersion.objects.create(
            author=cls.operator,
            document=cls.document,
            file_resource=cls.file
        )
        cls.documents_version2 = DocumentVersion.objects.create(
            author=cls.operator,
            document=cls.document,
            file_resource=cls.file
        )
        # 5. setup Transactions
        cls.valid_transaction = DocumentVersionTransaction.objects.create(
            author_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            transaction_address='0xacfa697d0aa65d1a8f533f198ac0499ee866d9bf24240a99bd67e10cee6ff6c0',
            hash_fingerprint=b'U\xef7>X\xc4\xd3\x08\x96zE\xf3 \xe7\x95\x85\xd5\xdd\x829\xabu"f\xb8Bl\xdb\x12v\xa7\x98',
            download_url='https://siteurl.com/version/57',
            document_version=cls.documents_version,
        )
        cls.invalid_transaction = DocumentVersionTransaction.objects.create(
            author_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            transaction_address='0xacfa697d0aa65d1a8f533f198ac0499ee866d9bf24240a99bd67e10cee6ff6c0',
            hash_fingerprint=b"|C\xca~\x0cbm'\x10\xf6:\x93)\xd5\xd0P\xbf\x8bRP\xc8Q\xc3|\xf6\xf1q\xe2S\x96\xdb\xc9",
            download_url='https://siteurl.com/version/57',
            document_version=cls.documents_version2
        )
        # 6. setup sc
        cls.document_sc = DocumentSC.objects.create(
            author_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            transaction_address='0x65138ba4ea251D8E96DB11cEad9285EE66039157',
            document=cls.document
        ),
        cls.document2_sc = DocumentSC.objects.create(
            author_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            transaction_address='0x65138ba4ea251D8E96DB11cEad9285EE66039151',
            document=cls.document2
        ),
