#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.db import models
from django.utils.timezone import now

from user.models import PaOperator, Citizen


class Document(models.Model):
    """
        Document model
        It represent a container of Document version.
        At the Document model are associated document title and description, favorites and view permissions
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, null=False)
    description = models.TextField(null=True, max_length=500)
    author = models.ForeignKey(PaOperator, null=False, on_delete=models.RESTRICT)
    require_permission = models.BooleanField(null=False, default=True)

    def __str__(self):
        """
        To string method
        :return: the document id and title
        """
        return str(self.id) + " - " + self.title

    def create_document(self, title, author, description=None, require_permission=True):
        """
        Create a new document
        :param title: the title of the document
        :param description: the description of the document
        :param author: the PA operator that required the creation
        :param require_permission: a flag that indicates if the document il public for all citizen or requires
        permissions
        :return:
        """
        self.title = title
        self.description = description
        self.author = author
        self.require_permission = require_permission
        self.save()
        return

    @staticmethod
    def get_document_list():
        """
        Return the list of the documents
        :return:
        """
        return Document.objects.all()


class DocumentVersion(models.Model):
    """
        Document Version model
        It specifies a version for the given document
        Version contains a file resource and a timestamp
        Author of the version may be different from document author
    """

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(PaOperator, null=False, on_delete=models.RESTRICT)
    creation_timestamp = models.DateTimeField(null=False, default=now)
    file_resource = models.FileField(default=None)
    document = models.ForeignKey(Document, null=False, on_delete=models.RESTRICT)

    indexes = [
        models.Index(fields=['creation_timestamp', ]),
    ]

    def __str__(self):
        """
        To string method
        :return: the document id and timestamp
        """
        return str(self.document.id) + " - " + str(self.creation_timestamp)

    def create_version(self, author, document, file_resource):
        """
        Create a new document version
        :param author: tha PA operator that requires creation
        :param document: the Document container
        :param file_resource: The attached file
        :return:
        """
        self.author = author
        self.document = document
        self.file_resource = file_resource
        self.save()
        return

    @staticmethod
    def get_versions_list(document):
        """
        Returns the list of version for a given document
        :param document: the Document container
        :return: the list of the version for the given Document
        """
        return DocumentVersion.objects.filter(document=document)

    @staticmethod
    def get_first_version(document):
        """
        Returns the first version of a given document
        :param document: the Document container
        :return: the first version of a given document
        """
        queryset = DocumentVersion.objects.filter(document=document).order_by("creation_timestamp")
        if queryset.exists():
            return queryset.first()
        return None

    @staticmethod
    def get_last_version(document):
        """
        Returns the last version of a given document
        :param document: the Document container
        :return: the last version of a given document
        """
        queryset = DocumentVersion.objects.filter(document=document).order_by("creation_timestamp")
        if queryset.exists():
            return queryset.last()
        return None

    def get_previous_version(self):
        """
        Returns the previous version of a given document version
        :return: the previous version of a given document version
        """
        queryset = DocumentVersion.objects.filter(document=self.document,
                                                  creation_timestamp__lt=self.creation_timestamp).order_by(
            "creation_timestamp")
        if queryset.exists():
            return queryset.last()
        return None

    def get_subsequent_version(self):
        """
        Returns the subsequent version of a given document version
        :return: the subsequent version of a given document version
        """
        queryset = DocumentVersion.objects.filter(document=self.document,
                                                  creation_timestamp__gt=self.creation_timestamp).order_by(
            "creation_timestamp")
        if queryset.exists():
            return queryset.first()
        return None


class Permission(models.Model):
    """
        Permission
        It represent the view permission for a given document and a given citizen
    """

    id = models.AutoField(primary_key=True)
    citizen = models.ForeignKey(Citizen, null=False, on_delete=models.RESTRICT)
    document = models.ForeignKey(Document, null=False, on_delete=models.RESTRICT)

    class Meta:
        unique_together = (('citizen', 'document'),)

    def add_permissions(self, citizen, document):
        """
        Add view permissions given a citizen and a document
        :param citizen: the citizen who want to grant permissions
        :param document: the document object of permissions
        :return:
        """
        self.citizen = citizen
        self.document = document
        self.save()
        return

    @staticmethod
    def remove_permissions(citizen, document):
        """
        Remove view permissions given a citizen and a document
        :param citizen: the citizen who want to remove permissions
        :param document: the document object of permissions
        :return:
        """
        queryset = Permission.objects.filter(citizen=citizen, document=document)
        if queryset.exists():
            queryset.delete()
        return

    @staticmethod
    def check_permissions(citizen, document):
        """
        Check view permissions given a citizen and a document
        :param citizen: the citizen who want to check permissions
        :param document: the document object of permissions
        :return:
        """
        return Permission.objects.filter(citizen=citizen, document=document).exists()


