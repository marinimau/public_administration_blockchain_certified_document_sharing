#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers

from contents.messages.get_messages import get_document_messages
from document.models import Document
from user.models import PaOperator, Citizen

document_messages = get_document_messages()


def validate_author(context):
    """
    Return the author of the document or raise a serialization error if it's not valid
    :param context: the request context
    :return: the author of the document or raise a serialization error if it's not valid
    """
    request = context.get("request")
    if request and hasattr(request, "user") and PaOperator.objects.filter(username=request.user.username).exists():
        return PaOperator.objects.get(username=request.user.username)
    error = {'message': document_messages['invalid_operator_error']}
    raise serializers.ValidationError(error)


def validate_citizen(cf):
    """
    Return a citizen object associated to the CF or raise a serialization error
    :param cf: the citizen cf code
    :return: a citizen object associated to the request username or raise a serialization error
    """
    if Citizen.check_if_exists(cf=cf):
        return Citizen.objects.get(cf=cf)
    error = {'message': document_messages['invalid_citizen_error']}
    raise serializers.ValidationError(error)


def validate_citizen_from_request(context):
    """
    Return a citizen object associated to the request or raise a serialization error
    :param context: the request context
    :return: a citizen object associated to the request username or raise a serialization error
    """
    request = context.get("request")
    if request and hasattr(request, "user") and Citizen.objects.filter(username=request.user.username).exists():
        return Citizen.objects.get(username=request.user.username)
    error = {'message': document_messages['invalid_citizen_error']}
    raise serializers.ValidationError(error)


def validate_document(document_id, queryset=Document.objects):
    """
    Return the document associated to the id or raise a serialization error if not exists
    :param document_id: the request context
    :param queryset: the documents queryset
    :return: the document associated to the id or raise a serialization error if not exists
    """
    if queryset.filter(id=document_id):
        return queryset.get(id=document_id)
    error = {'message': document_messages['document_not_exists_error']}
    raise serializers.ValidationError(error)

