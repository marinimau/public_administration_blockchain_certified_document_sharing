#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Document, DocumentVersion, Favorite, Permission
from ..user.models import PaOperator, Citizen, PublicAuthority

factory = APIRequestFactory()

RANGE_MAX = 3
RANGE_MAX_DOCUMENTS = 5
RANGE_MAX_DOCUMENT_VERSIONS = 8
RANGE_MAX_PERMISSIONS = 2
RANGE_MAX_FAVORITES = 6


class TestAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set-up the data for the test
        :return:
        """
        # 1. Setup Public Authorities
        cls.public_authorities = [PublicAuthority.objects.create(name=('Authority' + str(i))) for i in range(RANGE_MAX)]

        # 2. Setup PA operators
        cls.pa_operators = [PaOperator.objects.create(
            username=('operator' + str(i)),
            email=('operator' + str(i) + '@operators.com'),
            password='test',
            is_active=True,
            operator_code=('OP' + str(i)),
            public_authority=cls.public_authorities[i],
            bc_address='0x0000000000000000000000000000000000000000',
            bc_secret_key='secret'
        ) for i in range(RANGE_MAX)]
        [pa.set_password('PaOperator123.') for pa in cls.pa_operators]

        # 2. Setup Citizens
        cls.citizens = [Citizen.objects.create(
            username=('citizen' + str(i)),
            email=('citizen' + str(i) + '@citizen.com'),
            password='test',
            is_active=True,
            cf=('ctzctz00c00c000' + str(i)),
            region=Citizen.Regions.SIC
        ) for i in range(RANGE_MAX)]
        [c.set_password('Citizen123.') for c in cls.citizens]

        # 3. Setup Documents
        cls.documents = [Document.objects.create(
            title=('Document ' + str(i)),
            description=('This is the description of the document ' + str(i)),
            author=cls.pa_operators[i % RANGE_MAX],
            require_permission=(True if i % RANGE_MAX == 0 else False)
        ) for i in range(RANGE_MAX_DOCUMENTS)]

        # 4. Setup Document Versions
        cls.documents_versions = [DocumentVersion.objects.create(
            author=cls.pa_operators[i % RANGE_MAX],
            document=cls.documents[i % RANGE_MAX_DOCUMENTS],
        ) for i in range(RANGE_MAX_DOCUMENT_VERSIONS)]

        # 5. Setup Permissions
        cls.permissions = [Permission.objects.create(
            citizen=cls.citizens[i % RANGE_MAX],
            document=cls.documents[i % RANGE_MAX_DOCUMENTS]
        ) for i in range(RANGE_MAX_PERMISSIONS)]

        # 6. Setup Favorites
        cls.favorites = [Favorite.objects.create(
            citizen=cls.citizens[i % RANGE_MAX],
            document=cls.documents[i % RANGE_MAX_DOCUMENTS]
        ) for i in range(RANGE_MAX_FAVORITES)]

    def test_check_created_data(self):
        """
        Check the data created by setUpTestData
        :return:
        """
        self.assertEqual(len(self.public_authorities), RANGE_MAX)
        self.assertEqual(len(self.pa_operators), RANGE_MAX)
        self.assertEqual(len(self.citizens), RANGE_MAX)
        self.assertEqual(len(self.documents), RANGE_MAX_DOCUMENTS)
        self.assertEqual(len(self.documents_versions), RANGE_MAX_DOCUMENT_VERSIONS)
        self.assertEqual(len(self.permissions), RANGE_MAX_PERMISSIONS)
        self.assertEqual(len(self.favorites), RANGE_MAX_FAVORITES)
