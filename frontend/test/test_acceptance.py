#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 10/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.test import TestCase, Client

from api.document.models import DocumentVersion
from api.document.test.abstract_document_test import DocumentTestAbstract


class FrontendTestAcceptance(DocumentTestAbstract, TestCase):
    """
    Acceptance test class for frontend
    """

    def setUp(self):
        """
        Setup method
        :return:
        """
        self.documents_versions += [DocumentVersion.objects.create(
            author=self.pa_operators[0],
            document=self.documents[1],
        ) for _ in range(self.RANGE_MAX_DOCUMENT_VERSIONS)]
        self.client = Client()

    def test_check_created_data(self):
        """
        Check the data created by setUpTestData
        :return:
        """
        self.assertEqual(len(self.public_authorities), self.RANGE_MAX)
        self.assertEqual(len(self.pa_operators), self.RANGE_MAX)
        self.assertEqual(len(self.citizens), self.RANGE_MAX)
        self.assertEqual(len(self.documents), self.RANGE_MAX_DOCUMENTS)
        self.assertEqual(len(self.documents_versions), self.RANGE_MAX_DOCUMENT_VERSIONS * 2)
        self.assertEqual(len(self.permissions), self.RANGE_MAX_DOCUMENTS - 1)
        self.assertEqual(len(self.favorites), self.RANGE_MAX_DOCUMENTS - 1)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Document
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #   document list
    # ------------------------------------------------------------------------------------------------------------------

    def test_document_list(self):
        """
        Test the document list page not authenticated
        :return:
        """
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertLess(len(response.context['documents']), self.RANGE_MAX_DOCUMENTS)  # only public documents are shown

    # ------------------------------------------------------------------------------------------------------------------
    #   document detail
    # ------------------------------------------------------------------------------------------------------------------

    def test_document_detail(self):
        """
        Test the document detail page not authenticated
        :return:
        """
        response = self.client.get('/2', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['versions']), self.RANGE_MAX_DOCUMENT_VERSIONS)

    def test_document_detail_private_not_viewable_document(self):
        """
        Test the document detail page not authenticated
        :return:
        """
        response = self.client.get('/1', follow=True)
        self.assertEqual(response.status_code, 404)

    # ------------------------------------------------------------------------------------------------------------------
    #   document  version detail
    # ------------------------------------------------------------------------------------------------------------------

    def test_document_version_detail(self):
        """
        Test the document detail page not authenticated
        :return:
        """
        response = self.client.get('/version/11', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_document_version_detail_fail_document_private(self):
        """
        Test the document detail page not authenticated
        :return:
        """
        response = self.client.get('/version/8', follow=True)
        self.assertEqual(response.status_code, 404)  # associate to document 1 (private)






