#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers

from contents.messages.get_messages import get_generic_messages
from .models import DocumentSC, DocumentVersionTransaction

generic_messages = get_generic_messages()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document SC Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentSCSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSC
        fields = ['id', 'transaction_address', 'author_address', 'creation_timestamp', 'document']
        read_only_fields = ['id', 'transaction_address', 'author_address', 'creation_timestamp', 'document']


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version Transaction Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentVersionTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersionTransaction
        fields = '__all__'
