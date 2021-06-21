#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from user.models import Citizen, PaOperator
from .models import Document, Permission, Favorite, DocumentVersion
from .permissions import IsPaOperator, IsCitizen, IsOwner, IsOperatorSamePublicAuthority, DocumentPermissions
from .querysets import document_queryset, document_version_queryset
from .serializers import DocumentSerializer, PermissionSerializer, FavoriteSerializer, DocumentVersionSerializer, \
    FavoriteSerializer2, DocumentSerializerReadOnly
from contents.messages.get_messages import get_document_messages

document_messages = get_document_messages()


# ----------------------------------------------------------------------------------------------------------------------
#   Document views
#   -   documents list
#       - if GET:   list all documents object
#       - if POST:  create document
#   -   document detail:
#       - if GET: show document detail
#       - if PUT, UPDATE or DELETE:
# ----------------------------------------------------------------------------------------------------------------------


class DocumentsViewSet(viewsets.ModelViewSet):
    """
    Endpoint for the list of all the Documents
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializerReadOnly
    permission_classes = [DocumentPermissions]

    def perform_create(self, serializer):
        """
        Pass custom parameter to serializer
        :param serializer: the serializer
        :return:
        """
        serializer.save(author=PaOperator.objects.get(id=self.request.user.id))

    def get_queryset(self):
        """
        Get only documents of the same public authority
        :return:
        """
        return document_queryset(self)

    def get_serializer_class(self):
        """
        Get different serializer for post request
        :return: the serializer
        """
        if self.request.method == 'POST':
            return DocumentSerializer
        return DocumentSerializerReadOnly


# ----------------------------------------------------------------------------------------------------------------------
#   Document Version views
#   -   documents versions list
#       - if GET:   list all versions of a document
#
#   -   documents versions creation
#       - if POST:  create a version
#
#   -   document version detail:
#       - if GET: show document version detail
# ----------------------------------------------------------------------------------------------------------------------

class DocumentsVersionList(generics.ListCreateAPIView):
    """
    Endpoint for the list of all the Documents
    """
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [IsOperatorSamePublicAuthority]

    def perform_create(self, serializer):
        serializer.save(document_id=self.kwargs['document_id'])

    def get_queryset(self):
        """
        Get the version associated to the given document
        :return:
        """
        return document_version_queryset(self)


class DocumentVersionDetail(generics.RetrieveAPIView):
    """
    Endpoint for the single document version page
    """
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Get the version associated to the given document
        :return:
        """
        return document_version_queryset(self)


# ----------------------------------------------------------------------------------------------------------------------
#   Permission views
#   -   Permissions list of a document
#       - if GET:   list all user that can view a document
#
#   -   Permissions list of an user
#       - if GET:   list all user that can view a document
#
#   -   Permission creation
#       - if POST:  create permission
#
#   -   Permission detail:
#       - if GET: show permission detail
#       - if DELETE: delete permission
# ----------------------------------------------------------------------------------------------------------------------

class PermissionListDocument(generics.ListAPIView):
    """
    Endpoint for the list of permissions for a Document
    """
    queryset = Document.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsPaOperator]
    lookup_fields = 'citizen'

    def get_queryset(self):
        """
        Get the permissions associated to the given document
        :return:
        """
        document_id = self.kwargs['document_id']
        operator = PaOperator.objects.get(username=self.request.user.username)
        public_authority_documents = Document.objects.filter(author__public_authority=operator.public_authority)
        exists_document = public_authority_documents.filter(id=document_id).exists()
        if exists_document:
            document = Document.objects.get(id=document_id)
            return Permission.objects.filter(document=document)
        return []


class PermissionListUser(generics.ListAPIView):
    """
    Endpoint for the list of permissions for a Citizen
    """
    queryset = Document.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsPaOperator]
    lookup_fields = 'citizen'

    def get_queryset(self):
        """
        Get the permissions associated to the given citizen
        :return:
        """
        cf = self.kwargs['cf']
        cf = str.lower(cf)
        exists_citizen = Citizen.objects.filter(cf=cf).exists()
        if exists_citizen:
            citizen = Citizen.objects.get(cf=cf)
            operator = PaOperator.objects.get(username=self.request.user.username)
            return Permission.objects.filter(citizen=citizen,
                                             document__author__public_authority=operator.public_authority)
        return []


class PermissionCreation(generics.CreateAPIView):
    """
    Endpoint for the permission creation
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsPaOperator]


class PermissionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Serializer for the single document page
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsPaOperator]

    def get_queryset(self):
        """
        Get the permissions associated to document of the same public authority of the operator
        :return:
        """
        operator = PaOperator.objects.get(username=self.request.user.username)
        return Permission.objects.filter(document__author__public_authority=operator.public_authority)


# ----------------------------------------------------------------------------------------------------------------------
#   Favorite views
#   -   Favorite citizen list
#       - if GET:   list all favorite documents of the authenticated citizen
#       - if POST: add a document to favorites
#   -   Favorite item detail:
#       - if GET: show Favorite item detail
#       - if DELETE: remove document from favorites
# ----------------------------------------------------------------------------------------------------------------------


class FavoriteOfCitizenList(generics.ListCreateAPIView):
    """
    Endpoint for the list of all the favorite documents of the authenticated citizen
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer2
    permission_classes = [IsCitizen]
    lookup_fields = 'citizen'

    def perform_create(self, serializer):
        """
        Auto get citizen from request
        :param serializer:
        :return:
        """
        serializer.save(citizen=Citizen.objects.get(username=self.request.user.username))

    def get_queryset(self):
        """
        Get the likes associated to the given citizen
        :return:
        """
        user = self.request.user
        exists_citizen = user is not None and Citizen.objects.filter(username=user.username).exists()
        if exists_citizen:
            citizen = Citizen.objects.get(username=user.username)
            return Favorite.objects.filter(citizen=citizen)
        return []


class FavoriteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint for the single favorite page
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer2
    permission_classes = [IsCitizen]

    def get_queryset(self):
        """
        Get the likes associated to the given citizen
        :return:
        """
        citizen = Citizen.objects.get(username=self.request.user.username)
        return Favorite.objects.filter(citizen=citizen)


# ----------------------------------------------------------------------------------------------------------------------
#
#   404 error
#
# ----------------------------------------------------------------------------------------------------------------------

@api_view()
def error_page(request):
    """
    404 json response
    :param request: the request
    :return: a 404 error response with a custom message
    """
    return Response({'detail': document_messages['404_error']}, status=HTTP_404_NOT_FOUND)
