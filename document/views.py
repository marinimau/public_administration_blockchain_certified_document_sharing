#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from .models import Document
from .permissions import IsPaOperator, DocumentItemPermissions
from .serializers import DocumentSerializer
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


class DocumentsList(generics.ListCreateAPIView):
    """
    Serializer for the list of all the Documents
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsPaOperator]


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Serializer for the single document page
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DocumentItemPermissions]


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
