#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.test import TestCase
from django.urls import ResolverMatch
from django.http import HttpRequest

from api.document.test.abstract_document_test import DocumentTestAbstract
from ..permissions import *
from ..querysets import *


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
    #   DocumentPermissions - List
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

    # ------------------------------------------------------------------------------------------------------------------
    #   DocumentPermissions - obj
    # ------------------------------------------------------------------------------------------------------------------

    def test_document_detail_permission_update_ok(self):
        """
        Testing "DocumentPermission" custom permission - update detail (ok)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'PUT'
        request.user = self.pa_operators[0]
        obj = self.documents[0]
        result = document_permissions.has_object_permission(request, None, obj)
        self.assertTrue(result)

    def test_document_detail_permission_update_fail_operator_in_different_pa(self):
        """
        Testing "DocumentPermission" custom permission - update detail (fail, the operator is in a different PA)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'PUT'
        request.user = self.pa_operators[1]
        obj = self.documents[0]
        result = document_permissions.has_object_permission(request, None, obj)
        self.assertFalse(result)

    def test_document_detail_permission_update_fail_citizen(self):
        """
        Testing "DocumentPermission" custom permission - update detail (fail, citizen can only read)
        :return:
        """
        document_permissions = DocumentPermissions()
        request = HttpRequest()
        request.method = 'PUT'
        request.user = self.citizens[1]
        obj = self.documents[0]
        result = document_permissions.has_object_permission(request, None, obj)
        self.assertFalse(result)

    # ------------------------------------------------------------------------------------------------------------------
    #   DocumentVersionPermissions - list
    # ------------------------------------------------------------------------------------------------------------------

    def test_document_version_permission_post_ok(self):
        """
        Testing "DocumentPermission" custom permission - post (ok)
        :return:
        """
        document_version_permissions = DocumentVersionPermission()
        request = HttpRequest()
        request.method = 'POST'
        request.resolver_match = ResolverMatch(None, None, {'document_id': 1})
        request.user = self.pa_operators[0]
        result = document_version_permissions.has_permission(request, None)
        self.assertTrue(result)

    def test_document_version_permission_post_fail_different_pa(self):
        """
        Testing "DocumentPermission" custom permission - post (fail different pa)
        :return:
        """
        document_version_permissions = DocumentVersionPermission()
        request = HttpRequest()
        request.method = 'POST'
        request.resolver_match = ResolverMatch(None, None, {'document_id': 1})
        request.user = self.pa_operators[1]
        result = document_version_permissions.has_permission(request, None)
        self.assertFalse(result)

    def test_document_version_permission_post_fail_is_citizen(self):
        """
        Testing "DocumentPermission" custom permission - post (fail is citizen)
        :return:
        """
        document_version_permissions = DocumentVersionPermission()
        request = HttpRequest()
        request.resolver_match = ResolverMatch(None, None, {'document_id': 1})
        request.user = self.citizens[0]
        result = document_version_permissions.has_permission(request, None)
        self.assertFalse(result)

    def test_document_version_permission_post_fail_no_auth(self):
        """
        Testing "DocumentPermission" custom permission - post (fail is citizen)
        :return:
        """
        document_version_permissions = DocumentVersionPermission()
        request = HttpRequest()
        request.method = 'POST'
        request.resolver_match = ResolverMatch(None, None, {'document_id': 1})
        request.user = None
        result = document_version_permissions.has_permission(request, None)
        self.assertFalse(result)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Queryset test
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #   Viewable Document
    # ------------------------------------------------------------------------------------------------------------------

    def test_document_queryset_op1(self):
        """
        The the document queryset as operator1 (return all documents)
        :return:
        """
        request = HttpRequest()
        request.user = self.pa_operators[0]
        results = document_queryset(request)
        self.assertEqual(len(results), self.RANGE_MAX_DOCUMENTS)

    def test_document_queryset_op2(self):
        """
        The the document queryset as operator2 (return only public documents)
        :return:
        """
        request = HttpRequest()
        request.user = self.pa_operators[1]
        results = document_queryset(request)
        self.assertLess(len(results), self.RANGE_MAX_DOCUMENTS)
        for d in results:
            self.assertFalse(d.require_permission)

    def test_document_queryset_citizen1(self):
        """
        The the document queryset as citizen1 (return all document, we have create permissions)
        :return:
        """
        request = HttpRequest()
        request.user = self.citizens[0]
        results = document_queryset(request)
        self.assertEqual(len(results), self.RANGE_MAX_DOCUMENTS)

    def test_document_queryset_citizen2(self):
        """
        The the document queryset as citizen2 (return only public documents, citizen2 has not permissions)
        :return:
        """
        request = HttpRequest()
        request.user = self.citizens[1]
        results = document_queryset(request)
        self.assertLess(len(results), self.RANGE_MAX_DOCUMENTS)
        for d in results:
            self.assertFalse(d.require_permission)

    def test_document_queryset_no_auth(self):
        """
        The the document queryset whit no auth (return only public documents)
        :return:
        """
        request = HttpRequest()
        request.user = None
        results = document_queryset(request)
        self.assertLess(len(results), self.RANGE_MAX_DOCUMENTS)
        for d in results:
            self.assertFalse(d.require_permission)

    # ------------------------------------------------------------------------------------------------------------------
    #   Writeable Document
    # ------------------------------------------------------------------------------------------------------------------

    def test_document_queryset_write_op1(self):
        """
        The the document queryset as operator1 (return all documents)
        :return:
        """
        request = HttpRequest()
        request.user = self.pa_operators[0]
        results = document_write_queryset(request)
        self.assertEqual(len(results), self.RANGE_MAX_DOCUMENTS)

    def test_document_queryset_write_op2(self):
        """
        The the document queryset as operator2 (return 0 documents)
        :return:
        """
        request = HttpRequest()
        request.user = self.pa_operators[1]
        results = document_write_queryset(request)
        self.assertEqual(len(results), 0)

    def test_document_queryset_write_citizen1(self):
        """
        The the document queryset as citizen1 (return 0 documents)
        :return:
        """
        request = HttpRequest()
        request.user = self.citizens[0]
        results = document_write_queryset(request)
        self.assertEqual(len(results), 0)

    def test_document_queryset_write_no_auth(self):
        """
        The the document queryset with no auth (return 0 documents)
        :return:
        """
        request = HttpRequest()
        request.user = None
        results = document_write_queryset(request)
        self.assertEqual(len(results), 0)

    # ------------------------------------------------------------------------------------------------------------------
    #   Viewable DocumentVersions
    # ------------------------------------------------------------------------------------------------------------------

    class Caller:
        """
        Caller class
        """

        def __init__(self, request, kwargs):
            self.request = request
            self.kwargs = kwargs

    def test_document_version_queryset_op1(self):
        """
        The the document queryset as operator1 (return all documents)
        :return:
        """
        request = HttpRequest()
        kwargs = {'document_id': 1}
        request.user = self.pa_operators[0]
        results = document_version_queryset(self.Caller(request, kwargs))
        self.assertEqual(len(results), self.RANGE_MAX_DOCUMENT_VERSIONS)

    def test_document_versions_queryset_op2(self):
        """
        The the document version queryset as operator2 (return 0 versions, document is private)
        :return:
        """
        request = HttpRequest()
        kwargs = {'document_id': 1}
        request.user = self.pa_operators[1]
        results = document_version_queryset(self.Caller(request, kwargs))
        self.assertEqual(len(results), 0)

    def test_document_versions_queryset_citizen1(self):
        """
        The the document queryset as citizen1 (return all versions, citizen 1 has permission to view)
        :return:
        """
        request = HttpRequest()
        kwargs = {'document_id': 1}
        request.user = self.citizens[0]
        results = document_version_queryset(self.Caller(request, kwargs))
        self.assertEqual(len(results), self.RANGE_MAX_DOCUMENT_VERSIONS)

    def test_document_versions_queryset_citizen2(self):
        """
        The the document queryset as citizen2 (return 0, document is private and citizen 2 has not permission to view)
        :return:
        """
        request = HttpRequest()
        kwargs = {'document_id': 1}
        request.user = self.citizens[1]
        results = document_version_queryset(self.Caller(request, kwargs))
        self.assertEqual(len(results), 0)

    # ------------------------------------------------------------------------------------------------------------------
    #   Permissions
    # ------------------------------------------------------------------------------------------------------------------

    def test_permission_queryset_op1(self):
        """
        The the permission queryset as operator1 (return all permissions)
        :return:
        """
        request = HttpRequest()
        request.user = self.pa_operators[0]
        results = permission_all_queryset(self.Caller(request, None))
        self.assertEqual(len(results), self.RANGE_PERMISSIONS_MAX)

    def test_permission_queryset_op2(self):
        """
        The the permission queryset as operator2 (return 0 permissions)
        :return:
        """
        request = HttpRequest()
        request.user = self.pa_operators[1]
        results = permission_all_queryset(self.Caller(request, None))
        self.assertEqual(len(results), 0)
