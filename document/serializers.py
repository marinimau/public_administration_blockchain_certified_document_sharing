#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers

from .validators import document_validators
from contents.messages.get_messages import get_generic_messages
from .models import Document

generic_messages = get_generic_messages()


class DocumentSerializer(serializers.Serializer):
    """
    Document serializer
    this is the serializer of the Document model
    """

    def update(self, instance, validated_data):
        """
        Update serializer (not permitted)
        :param instance: the document instance to update
        :param validated_data: the validate data
        :return: always an error message, it's impossible to update this model
        """
        error = {'message': generic_messages['update_not_allowed_error']}
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        """
        Creation serializer
        :param validated_data: the validated data
        :return: The created instance and 201 response or raise a serialization error
        """
        author = document_validators.validate_author(self.context)
        title = validated_data.pop('title')
        description = validated_data.pop('description')
        require_permissions = validated_data.pop('require_permissions')
        return Document.create_document(title, author, description, require_permissions)

    id = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.username')
    title = serializers.CharField(min_length=10, max_length=60, required=True)
    description = serializers.CharField(max_length=500, required=False, default="No description")
    require_permissions = serializers.BooleanField(required=False, default=True)
