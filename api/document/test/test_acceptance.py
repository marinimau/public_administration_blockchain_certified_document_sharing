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

from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import reverse, resolve

from api.document.test.abstract_document_test import DocumentTestAbstract
from api.document.views import DocumentsViewSet, DocumentsVersionViewSet, PermissionViewSet, FavoriteViewSet

factory = APIRequestFactory()


class DocumentTestAcceptance(DocumentTestAbstract):
    """
    Test acceptance for document app
    """

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Document
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #   document list
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_document_list_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('document-list'))
        view = DocumentsViewSet.as_view({'get': 'list'})
        return request, view

    def assert_all_documents(self, response):
        """
        Check if the response data contains all documents
        :param response: the response
        :return:
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), len(self.documents))

    def assert_only_public_documents(self, response):
        """
        Check if the response data contains only public documents
        :param response: the response
        :return:
        """
        self.assertEqual(response.status_code, 200)
        self.assertLess(len(response.data['results']), len(self.documents))
        # check if all document are public
        [self.assertFalse(d['require_permission']) for d in response.data['results']]

    def test_document_list_no_auth(self):
        """
        Get the document list with no auth (only public documents)
        :return:
        """
        request, view = self.get_document_list_request_and_view()
        response = view(request)
        self.assert_only_public_documents(response)

    def test_document_list_op1_auth(self):
        """
        Get the document list with op1 auth (all documents, operator 1 has created all the documents)
        :return:
        """
        request, view = self.get_document_list_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request)
        self.assert_all_documents(response)

    def test_document_list_op2_auth(self):
        """
        Get the document list with op2 auth (only public documents, there are no document created by op2)
        :return:
        """
        request = factory.get(reverse('document-list'))
        view = DocumentsViewSet.as_view({'get': 'list'})
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request)
        self.assert_only_public_documents(response)

    def test_document_list_citizen1_auth(self):
        """
        Get the document list with citizen1 auth (citizen1 has permission for all the documents)
        :return:
        """
        request, view = self.get_document_list_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request)
        self.assert_all_documents(response)

    def test_document_list_citizen2_auth(self):
        """
        Get the document list with citizen2 auth (citizen2 has no permission, he can see only public documents)
        :return:
        """
        request, view = self.get_document_list_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request)
        self.assert_only_public_documents(response)

    # ------------------------------------------------------------------------------------------------------------------
    #   document creation
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_document_creation_request_and_view(bad=False):
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        if not bad:
            request = factory.post(reverse('document-list'), {'title': 'new document'}, format='json')
        else:
            request = factory.post(reverse('document-list'), {'tilte': 'new document'}, format='json')
        view = DocumentsViewSet.as_view({'post': 'create'})
        return request, view

    def test_document_creation_no_auth(self):
        """
        Create a document with no auth (fails - 401)
        :return:
        """
        request, view = self.get_document_creation_request_and_view()
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_document_creation_operator_auth(self):
        """
        Create a document with operator auth (ok)
        :return:
        """
        request, view = self.get_document_creation_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_document_creation_citizen_auth(self):
        """
        Create a document with citizen auth (fails - 403)
        :return:
        """
        request, view = self.get_document_creation_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_document_creation_operator_auth_bad_request(self):
        """
        Create a document with operator auth (fails - 400)
        :return:
        """
        request, view = self.get_document_creation_request_and_view(bad=True)
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request)
        self.assertEqual(response.status_code, 400)

    # ------------------------------------------------------------------------------------------------------------------
    #   document detail - get
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_document_detail_get_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('document-detail', args=(0,)), format='json')
        view = DocumentsViewSet.as_view({'get': 'retrieve'})
        return request, view

    def test_get_document_detail_no_auth_public_document(self):
        """
        Get details of a public document without auth (ok)
        :return:
        """
        request, view = self.get_document_detail_get_request_and_view()
        response = view(request, pk=2)
        self.assertEqual(response.status_code, 200)

    def test_get_document_detail_no_auth_private_document(self):
        """
        Get details of a private document without auth (fails - 404)
        :return:
        """
        request, view = self.get_document_detail_get_request_and_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 404)

    def test_get_document_detail_op1_auth_private_document(self):
        """
        Get details of a private document with op1 (same PA) auth (ok)
        :return:
        """
        request, view = self.get_document_detail_get_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_get_document_detail_op2_auth_private_document(self):
        """
        Get details of a private document with op2 (different PA) auth (fails 404)
        :return:
        """
        request, view = self.get_document_detail_get_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 404)

    def test_get_document_detail_citizen1_auth_private_document(self):
        """
        Get details of a private document with citizen1 (has permission) auth (ok)
        :return:
        """
        request, view = self.get_document_detail_get_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_get_document_detail_citizen2_auth_private_document(self):
        """
        Get details of a private document with citizen2 (no permissions) auth (fails 404)
        :return:
        """
        request, view = self.get_document_detail_get_request_and_view()
        force_authenticate(request, user=self.citizens[2])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 404)

    # ------------------------------------------------------------------------------------------------------------------
    #   document detail - update
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_document_detail_update_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.put(reverse('document-detail', args=(0,)), data={'title': 'New title'}, format='json')
        view = DocumentsViewSet.as_view({'put': 'partial_update'})
        return request, view

    def test_update_document_detail_op1_auth_private_document(self):
        """
        Update details of a private document with op1 (same PA) auth (ok)
        :return:
        """
        request, view = self.get_document_detail_update_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'New title')

    def test_update_document_detail_op2_auth_private_document(self):
        """
        Update details of a private document with op2 (different PA) auth (fails - 404)
        :return:
        """
        request, view = self.get_document_detail_update_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 404)

    def test_update_document_detail_op2_auth_public_document(self):
        """
        Update details of a private document with op2 (different PA) auth (fails - 403)
        :return:
        """
        request, view = self.get_document_detail_update_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, pk=2)
        self.assertEqual(response.status_code, 403)

    def test_update_document_detail_citizen_auth_public_document(self):
        """
        Update details of a private document with citizen auth (fails - 403)
        :return:
        """
        request, view = self.get_document_detail_update_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request, pk=2)
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------------------------------------------------------
    #   document detail - get
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_document_detail_delete_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.delete(reverse('document-detail', args=(0,)), format='json')
        view = DocumentsViewSet.as_view({'delete': 'destroy'})
        return request, view

    def test_delete_document_op1_auth_private_document(self):
        """
        Update details of a private document with op1 (same PA) auth (fails - 403)
        :return:
        """
        request, view = self.get_document_detail_delete_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Document Version
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #   document version list
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_document_version_list_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('document-version-list', args=(1,)), format='json')
        view = DocumentsVersionViewSet.as_view({'get': 'list'})
        return request, view

    def assert_version_ok(self, response):
        """
        Check if the response data contains all documents
        :param response: the response
        :return:
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), len(self.documents_versions))  # all version same document

    def assert_no_versions(self, response):
        """
        Check if the response data contains 0 versions
        :param response: the response
        :return:
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_document_version_list_no_auth(self):
        """
        Get the document 2 version list with no auth (fail 0 versions)
        :return:
        """
        request, view = self.get_document_version_list_request_and_view()
        response = view(request, document_id=1)
        self.assert_no_versions(response)

    def test_document_version_list_pa1_auth(self):
        """
        Get the document 2 version list with pa1 (same PA) auth (ok)
        :return:
        """
        request, view = self.get_document_version_list_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, document_id=1)
        self.assert_version_ok(response)

    def test_document_version_list_pa2_auth(self):
        """
        Get the document 2 version list with pa2 (different PA) auth (fail 0 versions)
        :return:
        """
        request, view = self.get_document_version_list_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, document_id=1)
        self.assert_no_versions(response)

    def test_document_version_list_citizen1_auth(self):
        """
        Get the document 2 version list with citizen1 (has permission) auth (ok)
        :return:
        """
        request, view = self.get_document_version_list_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request, document_id=1)
        self.assert_version_ok(response)

    def test_document_version_list_citizen2_auth(self):
        """
        Get the document 2 version list with citizen2 (no permission) auth (fail 0 versions)
        :return:
        """
        request, view = self.get_document_version_list_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request, document_id=1)
        self.assert_no_versions(response)

    # ------------------------------------------------------------------------------------------------------------------
    #   document version create
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create_document_version_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.post(reverse('document-version-list', args=(1,)), follow=True, format='json')
        request.resolver_match = resolve(reverse('document-version-list', kwargs={'document_id': 1}))
        view = DocumentsVersionViewSet.as_view({'post': 'create'})
        return request, view

    def test_document_version_create_pa1_auth(self):
        """
        Create version for the document 1  with pa1 (same PA) auth (ok)
        :return:
        """
        request, view = self.create_document_version_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, document_id=1)
        self.assertEqual(response.status_code, 400)  # needs file

    def test_document_version_create_pa2_auth(self):
        """
        Create version for document 2 with pa2 (different PA) auth (fail - 403)
        :return:
        """
        request, view = self.create_document_version_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, document_id=1)
        self.assertEqual(response.status_code, 403)

    def test_document_version_create_citizen1_auth(self):
        """
        Create version for document 2 with citizen1 auth (fail - 403)
        :return:
        """
        request, view = self.create_document_version_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request, document_id=1)
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------------------------------------------------------
    #   document version detail
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_document_version_detail_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('document-version-detail', args=(1, 1,)), format='json')
        view = DocumentsVersionViewSet.as_view({'get': 'retrieve'})
        return request, view

    def test_document_version_detail_pa1_auth(self):
        """
        Get the document 1 version 1 detail with pa1 (same PA) auth (ok)
        :return:
        """
        request, view = self.get_document_version_detail_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, document_id=1, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_document_version_detail_pa2_auth(self):
        """
        Get the document 1 version 1 detail with pa2 (different PA) auth (fail 404)
        :return:
        """
        request, view = self.get_document_version_detail_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, document_id=1, pk=1)
        self.assertEqual(response.status_code, 404)

    def test_document_version_detail_citizen1_auth(self):
        """
        Get the document 1 version 1 detail with citizen1 (has permissions) auth (ok)
        :return:
        """
        request, view = self.get_document_version_detail_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request, document_id=1, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_document_version_detail_citizen2_auth(self):
        """
        Get the document 1 version 1 detail with citizen2 (no permissions) auth (fail 404)
        :return:
        """
        request, view = self.get_document_version_detail_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request, document_id=1, pk=1)
        self.assertEqual(response.status_code, 404)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Permissions
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #   permissions list
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_permissions_list_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('permission-list'), format='json')
        view = PermissionViewSet.as_view({'get': 'list'})
        return request, view

    def assert_all_permissions(self, response):
        """
        Check if the response data contains all documents
        :param response: the response
        :return:
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), len(self.permissions))  # all documents are owned by pa1

    def assert_no_permissions(self, response):
        """
        Check if the response data contains 0 versions
        :param response: the response
        :return:
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_permission_list_no_auth(self):
        """
        Get the permission list with no auth (fail 401)
        :return:
        """
        request, view = self.get_permissions_list_request_and_view()
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_permissions_list_pa1_auth(self):
        """
        Get the permission list with pa1 (same PA) auth (ok)
        :return:
        """
        request, view = self.get_permissions_list_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request)
        self.assert_all_permissions(response)

    def test_permissions_list_pa2_auth(self):
        """
        Get the permission list with pa2 (different PA) auth (0 permissions found)
        :return:
        """
        request, view = self.get_permissions_list_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request)
        self.assert_no_permissions(response)

    def test_permissions_list_citizen1_auth(self):
        """
        Get the permission list with citizen1 (can view document but not permissions) auth (fail 403)
        :return:
        """
        request, view = self.get_permissions_list_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_permissions_list_citizen2_auth(self):
        """
        Get the permission list with citizen2 (can't view neither document and permissions) auth (fail 403)
        :return:
        """
        request, view = self.get_permissions_list_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------------------------------------------------------
    #   permissions detail
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_permissions_detail_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('permission-detail', args=(1,)), format='json')
        view = PermissionViewSet.as_view({'get': 'retrieve'})
        return request, view

    def test_permission_detail_no_auth(self):
        """
        Get the permission detail with no auth (fail 401)
        :return:
        """
        request, view = self.get_permissions_detail_request_and_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 401)

    def test_permissions_detail_pa1_auth(self):
        """
        Get the permission detail with pa1 (same PA) auth (ok)
        :return:
        """
        request, view = self.get_permissions_detail_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_permissions_detail_pa2_auth(self):
        """
        Get the permission detail with pa2 (different PA) auth (fail 404)
        :return:
        """
        request, view = self.get_permissions_detail_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 404)

    def test_permissions_detail_citizen1_auth(self):
        """
        Get the permission detail with citizen1 (can view document but not permissions) auth (fail 403)
        :return:
        """
        request, view = self.get_permissions_list_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    def test_permissions_detail_citizen2_auth(self):
        """
        Get the permission detail with citizen2 (can't view neither document and permissions) auth (fail 403)
        :return:
        """
        request, view = self.get_permissions_detail_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------------------------------------------------------
    #   permissions creation
    # ------------------------------------------------------------------------------------------------------------------

    def create_permissions_request_and_view(self, bad=False):
        """
        Returns a tuple: request and view
        :param bad: a flag to generate a bad request
        :return: a tuple: request and view
        """
        if not bad:
            request = factory.post(reverse('permission-list'), data={'citizen': self.citizens[0].id,
                                                                     'document': self.documents[
                                                                         self.RANGE_MAX_DOCUMENTS - 1].id},
                                   format='json')
        else:
            request = factory.post(reverse('permission-list'),
                                   data={'citizen': self.citizens[0].id, 'document': self.documents[0].id},
                                   format='json')
        view = PermissionViewSet.as_view({'post': 'create'})
        return request, view

    def test_permission_creation_no_auth(self):
        """
        Create permission with no auth (fail 401)
        :return:
        """
        request, view = self.create_permissions_request_and_view()
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_create_permissions_op1_auth(self):
        """
        Create permission with op1 auth (ok)
        :return:
        """
        request, view = self.create_permissions_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_create_permissions_op1_auth_bad_request(self):
        """
        Create permission with op1 auth bad request (fail 400)
        :return:
        """
        request, view = self.create_permissions_request_and_view(bad=True)
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_create_permissions_op2_auth(self):
        """
        Create permission with op2 auth (fail 400 document is owned by op1's PA)
        :return:
        """
        request, view = self.create_permissions_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_create_permissions_citizen1_auth(self):
        """
        Create permission with citizen1 auth (fail, citizen cannot create permissions)
        :return:
        """
        request, view = self.create_permissions_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------------------------------------------------------
    #   permissions delete
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_permissions_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.delete(reverse('permission-detail', args=(1,)), format='json')
        view = PermissionViewSet.as_view({'delete': 'destroy'})
        return request, view

    def test_permission_delete_no_auth(self):
        """
        Delete permission with no auth (fail 401)
        :return:
        """
        request, view = self.delete_permissions_request_and_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 401)

    def test_permissions_delete_pa1_auth(self):
        """
        Delete permission with pa1 (same PA) auth (ok)
        :return:
        """
        request, view = self.delete_permissions_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 204)

    def test_permissions_delete_pa2_auth(self):
        """
        Delete permission with pa2 (different PA) auth (fail 404)
        :return:
        """
        request, view = self.delete_permissions_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 404)

    def test_permissions_delete_citizen1_auth(self):
        """
        Delete permission with citizen1 (can view document but not permissions) auth (fail 403)
        :return:
        """
        request, view = self.delete_permissions_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    def test_permissions_delete_citizen2_auth(self):
        """
        Delete permission with citizen2 (can't view neither document and permissions) auth (fail 403)
        :return:
        """
        request, view = self.delete_permissions_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Favorite
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #   favorite list
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_favorite_list_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('favorite-list'), format='json')
        view = FavoriteViewSet.as_view({'get': 'list'})
        return request, view

    def assert_all_favorites(self, response):
        """
        Check if the response data contains all favorites
        :param response: the response
        :return:
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), len(self.favorites))

    def assert_no_favorite(self, response):
        """
        Check if the response data contains 0 favorites (no favorites for citizen 2)
        :param response: the response
        :return:
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_favorite_list_no_auth(self):
        """
        Get the favorite list with no auth (fail 401)
        :return:
        """
        request, view = self.get_favorite_list_request_and_view()
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_favorite_list_pa1_auth(self):
        """
        Get the favorite list with pa1 (same PA) auth (fail 403)
        :return:
        """
        request, view = self.get_favorite_list_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_favorite_list_pa2_auth(self):
        """
        Get the favorite list with pa2 (fail 403)
        :return:
        """
        request, view = self.get_favorite_list_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_favorite_list_citizen1_auth(self):
        """
        Get the favorite list with citizen1 (ok, all favorites)
        :return:
        """
        request, view = self.get_favorite_list_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assert_all_favorites(response)

    def test_favorite_list_citizen2_auth(self):
        """
        Get the favorite list with citizen2 (ok but no favorites)
        :return:
        """
        request, view = self.get_favorite_list_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assert_no_favorite(response)

    # ------------------------------------------------------------------------------------------------------------------
    #   favorite detail
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_favorite_detail_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.get(reverse('favorite-detail', args=(1,)), format='json')
        view = FavoriteViewSet.as_view({'get': 'retrieve'})
        return request, view

    def test_favorite_detail_no_auth(self):
        """
        Get the favorite detail with no auth (fail 401)
        :return:
        """
        request, view = self.get_favorite_detail_request_and_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 401)

    def test_favorite_detail_pa1_auth(self):
        """
        Get the favorite detail with pa1 (same PA) auth (fail 403)
        :return:
        """
        request, view = self.get_favorite_detail_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    def test_favorite_detail_pa2_auth(self):
        """
        Get the favorite detail with pa2 (different PA) auth (fail 404)
        :return:
        """
        request, view = self.get_favorite_detail_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    def test_favorite_detail_citizen1_auth(self):
        """
        Get favorite detail with citizen1 (ok)
        :return:
        """
        request, view = self.get_favorite_detail_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_favorite_detail_citizen2_auth(self):
        """
        Get favorite detail with citizen2 (fail 404)
        :return:
        """
        request, view = self.get_favorite_detail_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 404)

    # ------------------------------------------------------------------------------------------------------------------
    #   favorite creation
    # ------------------------------------------------------------------------------------------------------------------

    def create_favorite_request_and_view(self, bad=False):
        """
        Returns a tuple: request and view
        :param bad: a flag to generate a bad request
        :return: a tuple: request and view
        """
        if not bad:
            request = factory.post(reverse('favorite-list'),
                                   data={'document': self.documents[self.RANGE_MAX_DOCUMENTS - 1].id}, format='json')
        else:
            request = factory.post(reverse('favorite-list'), data={'document': self.documents[0].id}, format='json')
        view = FavoriteViewSet.as_view({'post': 'create'})
        return request, view

    def test_favorite_creation_no_auth(self):
        """
        Create favorite with no auth (fail 401)
        :return:
        """
        request, view = self.create_favorite_request_and_view()
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_create_favorite_op1_auth(self):
        """
        Create favorite with op1 auth (fail 403)
        :return:
        """
        request, view = self.create_favorite_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_create_favorite_op2_auth(self):
        """
        Create favorite with op2 auth (fail 403)
        :return:
        """
        request, view = self.create_favorite_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_create_favorite_citizen1_auth(self):
        """
        Create favorite with citizen1 auth (ok)
        :return:
        """
        request, view = self.create_favorite_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_create_favorite_citizen1_auth_bad_request(self):
        """
        Create favorite with citizen1 auth (fail 400)
        :return:
        """
        request, view = self.create_favorite_request_and_view(bad=True)
        force_authenticate(request, user=self.citizens[0])
        response = view(request)
        self.assertEqual(response.status_code, 400)

    # ------------------------------------------------------------------------------------------------------------------
    #   favorite delete
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_favorites_request_and_view():
        """
        Returns a tuple: request and view
        :return: a tuple: request and view
        """
        request = factory.delete(reverse('favorite-detail', args=(1,)), format='json')
        view = FavoriteViewSet.as_view({'delete': 'destroy'})
        return request, view

    def test_favorite_delete_no_auth(self):
        """
        Delete favorite with no auth (fail 401)
        :return:
        """
        request, view = self.delete_favorites_request_and_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 401)

    def test_favorite_delete_pa1_auth(self):
        """
        Delete favorite with pa1 (same PA) auth (fail 403)
        :return:
        """
        request, view = self.delete_favorites_request_and_view()
        force_authenticate(request, user=self.pa_operators[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    def test_favorite_delete_pa2_auth(self):
        """
        Delete favorite with pa2 (different PA) auth (fail 403)
        :return:
        """
        request, view = self.delete_favorites_request_and_view()
        force_authenticate(request, user=self.pa_operators[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)

    def test_favorite_delete_citizen1_auth(self):
        """
        Delete favorite with citizen1 (ok)
        :return:
        """
        request, view = self.delete_favorites_request_and_view()
        force_authenticate(request, user=self.citizens[0])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 204)

    def test_favorite_delete_citizen2_auth(self):
        """
        Delete favorite with citizen2 (fail 404)
        :return:
        """
        request, view = self.delete_favorites_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 404)
