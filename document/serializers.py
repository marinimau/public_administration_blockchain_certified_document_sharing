#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers

from user.serializers import PaOperatorSerializer, CitizenSerializer
from . import validators
from contents.messages.get_messages import get_generic_messages, get_document_messages
from .models import Document, Permission, Favorite, DocumentVersion

generic_messages = get_generic_messages()
document_messages = get_document_messages()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentSerializer(serializers.ModelSerializer):
    """
    Document serializer
    this is the serializer of the Document model
    """

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'author']


class DocumentSerializerReadOnly(DocumentSerializer):
    """
    Document serializer for read request
    this is the serializer print also the operator data
    """
    author = PaOperatorSerializer()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentVersionSerializer(serializers.Serializer):
    """
    Document Version serializer
    this is the serializer of the DocumentVersion model
    """

    def update(self, instance, validated_data):
        """
        Update serializer (not permitted)
        :param instance: the instance to update
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
        resource = validated_data.pop('resource')
        author = validators.validate_author(context=self.context)
        queryset = Document.objects.filter(author__public_authority=author.public_authority)
        document_id = validated_data.pop('document_id')
        document = validators.validate_document(document_id=document_id, queryset=queryset)
        return DocumentVersion.create_version(author=author, document=document, file_resource=resource)

    id = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.username')
    creation_timestamp = serializers.DateTimeField(read_only=True, required=False)
    resource = serializers.FileField(write_only=True, use_url=True, required=True)  # write only
    file_resource = serializers.URLField(read_only=True)  # read only
    document = serializers.ReadOnlyField(source='document.id')


# ----------------------------------------------------------------------------------------------------------------------
#
#   Permissions Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class PermissionSerializer(serializers.ModelSerializer):
    """
    Permission serializer
    this is the serializer of the Permission model
    """

    class Meta:
        model = Permission
        fields = '__all__'
        read_only_fields = ['id', 'document', 'citizen']


class PermissionSerializerReadOnly(PermissionSerializer):
    """
    Permission serializer for read request
    this is the serializer print citizen data instead pk
    """
    citizen = CitizenSerializer()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Favorite Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class FavoriteSerializer(serializers.ModelSerializer):
    """
    Favorite serializer
    this is the serializer of the Favorite model
    """

    class Meta:
        model = Favorite
        fields = ['id', 'citizen', 'document']
        read_only_fields = ['id', 'citizen', 'document']


class FavoriteSerializerReadOnly(FavoriteSerializer):
    """
    Favorite serializer for read request
    shows document data instead pk
    """
    document = DocumentSerializer()
