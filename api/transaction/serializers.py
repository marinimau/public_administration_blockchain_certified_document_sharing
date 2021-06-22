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
from .models import DocumentTransaction, DocumentVersionTransaction

generic_messages = get_generic_messages()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Transaction Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTransaction
        fields = '__all__'


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version Transaction Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentVersionTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersionTransaction
        fields = '__all__'


