#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers

from api.user.serializers import PaOperatorSerializer, CitizenSerializer
from contents.messages.get_messages import get_generic_messages, get_document_messages
from .models import Document, Permission, Favorite, DocumentVersion
from .querysets import document_queryset

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

class DocumentVersionSerializer(serializers.ModelSerializer):
    """
    Document Version serializer
    this is the serializer of the DocumentVersion model
    """

    class Meta:
        model = DocumentVersion
        fields = '__all__'
        read_only_fields = ['id', 'document', 'author', 'creation_timestamp']

    def validate_document(self, value):
        if document_queryset(self.context['request']).filter(id=value.id).exists():
            raise serializers.ValidationError(document_messages['document_does_not_exists'])
        return value


class DocumentVersionSerializerReadOnly(DocumentVersionSerializer):
    """
    Document version serializer for read request
    this serializer print author data instead pk
    """
    author = PaOperatorSerializer()


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
        read_only_fields = ['id']

    def validate(self, data):
        if data['document'] not in document_queryset(self.context['request']):
            raise serializers.ValidationError(document_messages['document_does_not_exists'])
        return data


class PermissionSerializerReadOnly(PermissionSerializer):
    """
    Permission serializer for read request
    this serializer print citizen data instead pk
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
        read_only_fields = ['id', 'citizen']

    def validate(self, data):
        if data['document'] not in document_queryset(self.context['request']):
            raise serializers.ValidationError(document_messages['document_does_not_exists'])
        if Favorite.objects.filter(citizen__username=self.context['request'].user.username,
                                   document=data['document']).exists():
            raise serializers.ValidationError(document_messages['favorite_already_exists'])
        return data


class FavoriteSerializerReadOnly(FavoriteSerializer):
    """
    Favorite serializer for read request
    shows document data instead pk
    """
    document = DocumentSerializer()
