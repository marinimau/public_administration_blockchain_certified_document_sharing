"""
This software is distributed under MIT/X11 license

Copyright (c) 2021 Mauro Marini - University of Cagliari

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

from rest_framework import serializers

from api.user.serializers import PaOperatorSerializer, CitizenSerializer
from contents.messages.get_messages import get_generic_messages, get_document_messages
from .models import Document, Permission, Favorite, DocumentVersion
from .querysets import document_queryset, document_write_queryset
from ..transaction.serializers import DocumentSCSerializer, DocumentVersionTransactionSerializer

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
        fields = ['id', 'title', 'description', 'author', 'require_permission', 'document_sc']
        read_only_fields = ['id', 'author', 'document_sc']

    document_sc = DocumentSCSerializer(read_only=True)


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
        fields = ['id', 'document', 'author', 'creation_timestamp', 'file_resource', 'version_transaction']
        read_only_fields = ['id', 'document', 'author', 'creation_timestamp', 'version_transaction']

    version_transaction = DocumentVersionTransactionSerializer(read_only=True)

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
    document = DocumentSerializerReadOnly()


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
        if data['document'] not in document_write_queryset(self.context['request']):
            raise serializers.ValidationError(document_messages['document_does_not_exists'])
        else:
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
