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

    # ------------------------------------------------------------------------------------------------------------------
    #   isOwner
    # ------------------------------------------------------------------------------------------------------------------

    def test_permission_is_owner_permission_ok(self):
        """
        Testing "isOwner" custom permission (ok)
        :return:
        """
        is_owner = IsOwner()
        request = HttpRequest()
        request.user = self.citizens[0]
        obj = self.permissions[0]
        result = is_owner.has_object_permission(request, None, obj)
        self.assertTrue(result)

    def test_permission_is_owner_permission_fail_different_citizen(self):
        """
        Testing "isOwner" custom permission (fail)
        :return:
        """
        is_owner = IsOwner()
        request = HttpRequest()
        request.user = self.citizens[1]
        obj = self.permissions[0]
        result = is_owner.has_object_permission(request, None, obj)
        self.assertFalse(result)

    def test_permission_is_owner_permission_fail_different_operator(self):
        """
        Testing "isOwner" custom permission (fail)
        :return:
        """
        is_owner = IsOwner()
        request = HttpRequest()
        request.user = self.pa_operators[0]
        obj = self.permissions[0]
        result = is_owner.has_object_permission(request, None, obj)
        self.assertFalse(result)

    def test_permission_is_owner_favorite_ok(self):
        """
        Testing "isOwner" custom permission (ok)
        :return:
        """
        is_owner = IsOwner()
        request = HttpRequest()
        request.user = self.citizens[0]
        obj = self.favorites[0]
        result = is_owner.has_object_permission(request, None, obj)
        self.assertTrue(result)

    def test_permission_is_owner_favorite_fail_different_citizen(self):
        """
        Testing "isOwner" custom permission (fail)
        :return:
        """
        is_owner = IsOwner()
        request = HttpRequest()
        request.user = self.citizens[1]
        obj = self.favorites[0]
        result = is_owner.has_object_permission(request, None, obj)
        self.assertFalse(result)

    def test_permission_is_owner_favorite_fail_different_operator(self):
        """
        Testing "isOwner" custom permission (fail)
        :return:
        """
        is_owner = IsOwner()
        request = HttpRequest()
        request.user = self.pa_operators[0]
        obj = self.favorites[0]
        result = is_owner.has_object_permission(request, None, obj)
        self.assertFalse(result)

    # ------------------------------------------------------------------------------------------------------------------
    #   DocumentPermissions
    # ------------------------------------------------------------------------------------------------------------------

    def test_document_permission_post_ok(self):
        """
        Testing "DocumentPermission" custom permission - post (ok)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.pa_operators[0]
        result = document_permissions.has_permission(request, None)
        self.assertTrue(result)

    def test_document_permission_post_fail_is_citizen(self):
        """
        Testing "DocumentPermission" custom permission - post (fail, only an operator can create a document)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.citizens[0]
        result = document_permissions.has_permission(request, None)
        self.assertFalse(result)

    def test_document_permission_post_fail_no_auth(self):
        """
        Testing "DocumentPermission" custom permission - post (fail, only an operator can create a document)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'POST'
        request.user = None
        result = document_permissions.has_permission(request, None)
        self.assertFalse(result)

    def test_document_permission_get_no_auth(self):
        """
        Testing "DocumentPermission" custom permission - get (ok)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'GET'
        request.user = None
        result = document_permissions.has_permission(request, None)
        self.assertTrue(result)

    def test_document_permission_get_citizen_auth(self):
        """
        Testing "DocumentPermission" custom permission - get (ok)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'GET'
        request.user = self.citizens[0]
        result = document_permissions.has_permission(request, None)
        self.assertTrue(result)

    def test_document_permission_get_operator_auth(self):
        """
        Testing "DocumentPermission" custom permission - get (ok)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'GET'
        request.user = self.pa_operators[0]
        result = document_permissions.has_permission(request, None)
        self.assertTrue(result)