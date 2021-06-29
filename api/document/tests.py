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


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

class TestDocumentViewSet(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set-up the data for the test
        :return:
        """
        # 1. Setup Public Authorities
        cls.public_authorities = [PublicAuthority.objects.create(name=('Authority' + str(i))) for i in range(3)]

    def test_check_created_data(self):
        """
        Check the data created by setUpTestData
        :return:
        """
        self.assertEqual(len(self.public_authorities), 3)