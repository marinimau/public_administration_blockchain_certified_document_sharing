#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.test import TestCase

from api.document.test.abstract_document_test import DocumentTestAbstract
from ..permissions import *
from django.http import HttpRequest


class DocumentUnitTest(DocumentTestAbstract, TestCase):
    """
    Test unit for document app
    """

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Permission test
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #   isPaOperator
    # ------------------------------------------------------------------------------------------------------------------

    def test_permission_is_pa_operator_ok(self):
        """
        Testing "isPaOperator" custom permission (ok)
        :return:
        """
        is_pa_operator = IsPaOperator()
        request = HttpRequest()
        request.user = self.pa_operators[0]
        result = is_pa_operator.has_permission(request, None)
        self.assertTrue(result)

    def test_permission_is_pa_operator_fail_is_citizen(self):
        """
        Testing "isPaOperator" custom permission (fail)
        :return:
        """
        is_pa_operator = IsPaOperator()
        request = HttpRequest()
        request.user = self.citizens[0]
        result = is_pa_operator.has_permission(request, None)
        self.assertFalse(result)

    # ------------------------------------------------------------------------------------------------------------------
    #   isCitizen
    # ------------------------------------------------------------------------------------------------------------------

    def test_permission_is_pa_operator_fail_no_user(self):
        """
        Testing "isPaOperator" custom permission (fail)
        :return:
        """
        is_pa_operator = IsPaOperator()
        request = HttpRequest()
        request.user = None
        result = is_pa_operator.has_permission(request, None)
        self.assertFalse(result)

    def test_permission_is_citizen_ok(self):
        """
        Testing "isCitizen" custom permission (ok)
        :return:
        """
        is_citizen = IsCitizen()
        request = HttpRequest()
        request.user = self.citizens[0]
        result = is_citizen.has_permission(request, None)
        self.assertTrue(result)

    def test_permission_is_citizen_fail_is_operator(self):
        """
        Testing "isCitizen" custom permission (fail)
        :return:
        """
        is_citizen = IsCitizen()
        request = HttpRequest()
        request.user = self.pa_operators[0]
        result = is_citizen.has_permission(request, None)
        self.assertFalse(result)

    def test_permission_is_citizen_fail_no_user(self):
        """
        Testing "isCitizen" custom permission (fail)
        :return:
        """
        is_citizen = IsCitizen()
        request = HttpRequest()
        request.user = None
        result = is_citizen.has_permission(request, None)
        self.assertFalse(result)
