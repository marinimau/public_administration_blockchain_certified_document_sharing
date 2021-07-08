#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 08/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers

from contents.messages.get_messages import get_transaction_messages
from ...document.models import DocumentVersion

transaction_messages = get_transaction_messages()


def validate_version_id(version_id):
    """
    Validate the version id
    :param version_id: the version id
    :return: the version id or an error
    """
    try:
        version_id = int(version_id)
    except ValueError:
        raise serializers.ValidationError(transaction_messages['bad_version_id'])
    if version_id is not None and isinstance(version_id, int) and DocumentVersion.objects.filter(
            id=version_id).exists():
        return version_id
    else:
        raise serializers.ValidationError(transaction_messages['version_not_found'])


def get_validation_description(validation_flag):
    """
    Return the validation description from the validation flag
    :param validation_flag: the validation flag
    :return: the validation description
    """
    if validation_flag == -1:
        return 'ALTERED'
    elif validation_flag == 1:
        return 'VALIDATED'
    else:
        return 'UNAVAILABLE'
