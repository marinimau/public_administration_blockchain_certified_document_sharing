#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#
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
    def get_document_validation_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('document-version-validation'), {'document_version': 1})
        return request, validate_document

    def test_validate_file(self):
        """
        Test validate document version file (ok)
        """
        request, view = self.get_document_validation_view()
        response = view(request)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.data['status'], 'ALTERED')

    def test_validate_file_altered(self):
        """
        Test validate document version file (altered)
        """
        request, view = self.get_document_validation_view()
        response = view(request)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.data['status'], 'ALTERED')


