#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework.authtoken.models import Token
from django.urls import reverse

from .models import Document, DocumentVersion, Favorite, Permission
from .views import DocumentsViewSet, DocumentsVersionViewSet
from ..user.models import PaOperator, Citizen, PublicAuthority


factory = APIRequestFactory()

RANGE_MAX = 3
RANGE_MAX_DOCUMENTS = 5
RANGE_MAX_DOCUMENT_VERSIONS = 8


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
            bc_address='0x000000000000000000000000000000000000000' + str(i),
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
            author=cls.pa_operators[0],
            require_permission=(True if i % RANGE_MAX == 0 else False)
        ) for i in range(RANGE_MAX_DOCUMENTS)]

        # 4. Setup Document Versions
        cls.documents_versions = [DocumentVersion.objects.create(
            author=cls.pa_operators[0],
            document=cls.documents[i % RANGE_MAX_DOCUMENTS],
        ) for i in range(RANGE_MAX_DOCUMENT_VERSIONS)]

        # 5. Setup Permissions
        cls.permissions = [Permission.objects.create(
            citizen=cls.citizens[0],
            document=cls.documents[i % RANGE_MAX_DOCUMENTS]
        ) for i in range(RANGE_MAX_DOCUMENTS)]

        # 6. Setup Favorites
        cls.favorites = [Favorite.objects.create(
            citizen=cls.citizens[0],
            document=cls.documents[i % RANGE_MAX_DOCUMENTS]
        ) for i in range(RANGE_MAX_DOCUMENTS)]

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
        self.assertEqual(len(self.permissions), RANGE_MAX_DOCUMENTS)
        self.assertEqual(len(self.favorites), RANGE_MAX_DOCUMENTS)

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
        Create a document with no auth (fails - unauthorized)
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
        Create a document with citizen auth (fails - forbidden)
        :return:
        """
        request, view = self.get_document_creation_request_and_view()
        force_authenticate(request, user=self.citizens[1])
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_document_creation_operator_auth_bad_request(self):
        """
        Create a document with operator auth (fails - bad request)
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
        request = factory.get(reverse('document-detail', args=(0,)),   format='json')
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


    # document version - get
    # document version - create

    # permissions get
    # permission get by document
    # permission get by user
    # permission creation
    # permission detail
    # permission delete

    # favorite get
    # favorite add
    # favorite delete
    # favorite detail
