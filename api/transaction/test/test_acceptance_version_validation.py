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

from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .abstract_transaction_test import TransactionTestAbstract
from ..views import validate_document

factory = APIRequestFactory()


class TransactionTestAcceptance(TransactionTestAbstract):
    """
    Transaction test acceptance class
    """

    @staticmethod
    def get_document_validation_view(version_id=1):
        """
        Returns a tuple: request and view
        :param version_id: the od of the document version
        :return: a tuple: request and view
        """
        request = factory.get(reverse('document-version-validation'), {'document_version': version_id})
        return request, validate_document

    def test_validate_file(self):
        """
        Test validate document version file (ok)
        """
        request, view = self.get_document_validation_view(version_id=62)
        response = view(request)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.data['status'], 'VALIDATED')

    def test_validate_file_altered(self):
        """
        Test validate document version file (altered)
        """
        request, view = self.get_document_validation_view(version_id=1)
        response = view(request)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.data['status'], 'ALTERED')

    def test_validate_file_unavailable(self):
        """
        Test validate document version file (unavailable)
        """
        request, view = self.get_document_validation_view(version_id=3)
        response = view(request)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.data['status'], 'UNAVAILABLE')


