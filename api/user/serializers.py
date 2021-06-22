#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers

from api.user.models import PaOperator, Citizen


# ----------------------------------------------------------------------------------------------------------------------
#
#   PaOperator Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class PaOperatorSerializer(serializers.ModelSerializer):
    """
    PaOperator serializer
    this is the serializer of the PaOperator model
    """

    class Meta:
        model = PaOperator
        fields = ['operator_code', 'username', 'bc_address', 'public_authority']
        read_only_fields = ['operator_code', 'username', 'bc_address', 'public_authority']


# ----------------------------------------------------------------------------------------------------------------------
#
#   Citizen Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class CitizenSerializer(serializers.ModelSerializer):
    """
    Citizen serializer
    this is the serializer of the Citizen model
    """

    class Meta:
        model = Citizen
        fields = ['id', 'cf']
        read_only_fields = ['id', 'cf']

