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

from django.conf import settings
from django.core.files.base import ContentFile
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
        cls.documents_version2 = DocumentVersion.objects.create(
            author=cls.operator,
            document=cls.document,
        )
        cls.documents_version3 = DocumentVersion.objects.create(
            author=cls.operator,
            document=cls.document,
        )
        cls.documents_version_to_reach_correct_id = [DocumentVersion.objects.create(
            author=cls.operator,
            document=cls.document,
        ) for _ in range(59)]
        cls.documents_version = DocumentVersion.objects.create(
            author=cls.operator,
            document=cls.document,
        )
        cls.set_version_file(cls.documents_version)
        cls.set_version_file(cls.documents_version2)
        cls.set_version_file(cls.documents_version3)
        # 5. setup Transactions
        cls.valid_transaction = DocumentVersionTransaction.objects.create(
            author_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            transaction_address='0xc53364bd323d7299a37f149d7391c10068aa02913645c4a86a4c8106838ae793',
            hash_fingerprint=b'\xe0\x0eE%\xfa\xa9\x91\xb8"S\xc8ZF_\x85\xe7\xdfm\xcb\x98X_v\xd9\t\xf4\x05\x18vP\xdc\x03',
            download_url='https://siteurl.com/version/61',
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
            transaction_address='0x3CfF857728e9f1db164C75E8425f0F9eB1B392E3',
            document=cls.document
        ),
        cls.document2_sc = DocumentSC.objects.create(
            author_address='0x4939119b43AFBFaB397d4fa5c46A14f460B1a2E9',
            transaction_address='0x65138ba4ea251D8E96DB11cEad9285EE66039151',
            document=cls.document2
        ),

    @staticmethod
    def set_version_file(document_version):
        """
        Set the attached file tp the document version
        :param document_version:
        :return:
        """
        original_file_path = settings.STATICFILES_DIRS[0] + '/test/file.txt'
        new_file_path = 'file.txt'
        with open(original_file_path, "rb") as fh:
            with ContentFile(fh.read()) as file_content:
                document_version.file_resource.save(new_file_path, file_content)
                document_version.save()

