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
from .permissions import IsPaOperator, IsCitizen, IsOperatorSamePublicAuthority, DocumentPermissions
from .querysets import document_queryset, document_version_queryset, permission_all_queryset
from .serializers import DocumentSerializer, PermissionSerializer, DocumentVersionSerializer, \
    DocumentSerializerReadOnly, PermissionSerializerReadOnly, FavoriteSerializer, \
    FavoriteSerializerReadOnly
from contents.messages.get_messages import get_document_messages

document_messages = get_document_messages()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
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
        return document_queryset(self.request)

    def get_serializer_class(self):
        """
        Get different serializer for post request
        :return: the serializer
        """
        if self.request.method == 'POST':
            return DocumentSerializer
        return DocumentSerializerReadOnly


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentsVersionList(generics.ListCreateAPIView):
    """
    Endpoint Document Version
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
#
#   Permission
#
# ----------------------------------------------------------------------------------------------------------------------

class PermissionViewSet(viewsets.ModelViewSet):
    """
    Endpoint Permission
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializerReadOnly
    permission_classes = [IsPaOperator]

    def get_queryset(self):
        """
        Get the permissions associated to document of the same public authority of the operator
        :return:
        """
        queryset = permission_all_queryset(self)
        citizen = self.request.query_params.get('citizen')
        document = self.request.query_params.get('document')
        if document is not None:
            queryset = queryset.filter(document__id=document)
        if citizen is not None:
            queryset = queryset.filter(citizen__cf=citizen)
        return queryset

    def get_serializer_class(self):
        """
        Get different serializer for post request
        :return: the serializer
        """
        if self.request.method == 'POST':
            return PermissionSerializer
        return PermissionSerializerReadOnly


# ----------------------------------------------------------------------------------------------------------------------
#
#   Favorite
#
# ----------------------------------------------------------------------------------------------------------------------


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    Endpoint for Favorite
    """
    queryset = Permission.objects.all()
    serializer_class = FavoriteSerializerReadOnly
    permission_classes = [IsCitizen]

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
        username = self.request.user.username
        return Favorite.objects.filter(citizen__username=username)

    def get_serializer_class(self):
        """
        Get different serializer for post request
        :return: the serializer
        """
        if self.request.method == 'POST':
            return FavoriteSerializer
        return FavoriteSerializerReadOnly


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
