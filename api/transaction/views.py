#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from contents.messages.get_messages import get_transaction_messages
from .utils.integration import validate_document_version
from .utils.view_utils import *
from ..document.models import DocumentVersion

transaction_messages = get_transaction_messages()


@api_view()
def validate_document(request):
    """
    Return the document validation status
    :param request: the request
    :return: a tuple validation status, transaction address
    """
    document_version_id = validate_version_id(request.query_params.get('document_version', None))
    flag, address = validate_document_version(DocumentVersion.objects.get(id=document_version_id))
    return Response({"status": get_validation_description(flag), "address": str(address)})

