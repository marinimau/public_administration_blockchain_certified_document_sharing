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






