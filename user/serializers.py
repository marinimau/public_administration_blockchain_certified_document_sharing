#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers

from user.models import PaOperator


# ----------------------------------------------------------------------------------------------------------------------
#
#   PaOperator Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class PaOperatorSerializer(serializers.ModelSerializer):
    """
    Permission serializer
    this is the serializer of the Permission model
    """

    class Meta:
        model = PaOperator
        fields = ['operator_code', 'username', 'bc_address', 'public_authority']
        read_only_fields = ['operator_code', 'username', 'bc_address', 'public_authority']
