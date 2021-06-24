#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from gnosis.eth.django.models import EthereumAddressField

from django.db import models

# ----------------------------------------------------------------------------------------------------------------------
#
#   Abstract Transaction
#
# ----------------------------------------------------------------------------------------------------------------------
from api.document.models import Document, DocumentVersion


class AbstractTransaction(models.Model):
    """
    Abstract Transaction
    This class represent an abstract model of transaction
    DocumentTransaction model and DocumentVersionTransaction model extend this class
    """
    id = models.AutoField(primary_key=True)
    transaction_address = EthereumAddressField(null=False, unique=True)
    author_address = EthereumAddressField(null=False)
    creation_timestamp = models.DateField(null=False)

    class Meta:
        abstract = True

    def __str__(self):
        """
        To string method
        :return: The address of the transaction
        """
        return str(self.transaction_address)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Transaction
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentTransaction(AbstractTransaction):
    """
    Document Transaction
    This class represent the model of transaction for Document model
    """
    document = models.OneToOneField(Document, on_delete=models.RESTRICT)
    signature_secret_key = models.CharField(null=False, max_length=256, default='secret_key')
    signature_public_key = models.CharField(null=False, max_length=256, default='public_key')

    @staticmethod
    def create_document_transaction(document, operator):
        """
        Create the transaction of the document container
        :param document: a Document object
        :param operator: a PaOperator object
        :return: the created Document Transaction
        """
        pass

    @staticmethod
    def check_if_transaction_exists(document):
        """
        Given a document returns True if the transaction associated to the document exists, false otherwise
        :param document: a Document object
        :return: the transaction associated to the document
        """
        return DocumentTransaction.objects.filter(document=document).exists()

    @staticmethod
    def get_by_document(document):
        """
        Given a document returns the transaction associated to the document.
        :param document: a Document object
        :return: the transaction associated to the document
        """
        if DocumentTransaction.check_if_transaction_exists(document):
            return DocumentTransaction.objects.get(document=document)
        return None


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version Transaction
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentVersionTransaction(AbstractTransaction):
    """
    Document Version Transaction
    This class represent the model of transaction for Document Version model
    """

    class ValidationStatus(models.TextChoices):
        """
        Transaction status enumeration
        Valid only for document transaction
        """
        PENDING = 'PENDING'
        VALID = 'VALID'
        ALTERED = 'ALTERED'

    hash_fingerprint = models.CharField(max_length=256, null=False)
    document_version = models.OneToOneField(DocumentVersion, on_delete=models.RESTRICT, null=False)
    download_url = models.URLField(null=False)
    validation_status = models.CharField(null=False, max_length=7, choices=ValidationStatus.choices,
                                         default=ValidationStatus.PENDING)

    @staticmethod
    def create_document_version_transaction(document_version, operator):
        """
        Create the transaction of the document version
        :param document_version: a Document Version object
        :param operator: a PaOperator object
        :return: the created Document Version Transaction
        """
        # TODO:
        #   1. get the Document obj associated to the DocumentVersion obj
        #   2. generate the sha256 fingerprint of the file attached to the document
        #   3. get wallet credential from the PaOperator
        #   4. create the transaction on the BC
        #   5. store the created BC transaction on Django
        #
        pass

    @staticmethod
    def check_if_transaction_exists(document_version):
        """
        Given a document returns True if the transaction associated to the document version exists, false otherwise
        :param document_version: a DocumentVersion object
        :return: the transaction associated to the DocumentVersion object
        """
        return DocumentTransaction.objects.filter(document_version=document_version).exists()

    @staticmethod
    def get_by_document(document_version):
        """
        Given a document returns the transaction associated to the document version
        :param document_version: a DocumentVersion object
        :return: the transaction associated to the document
        """
        if DocumentTransaction.check_if_transaction_exists(document_version):
            return DocumentTransaction.objects.get(document_version=document_version)
        return None

    @staticmethod
    def validate_document_version(document_version):
        """
        Given a document returns the validation state
        :param document_version: a DocumentVersion object
        :return: the validation state
        """
        # TODO:
        #   1. get the transaction stored in the bc
        #   2. compare the stored fingerprint with the fingerprint calculated on the document_version.file_resource
        #   3. return the validation status
        #
        pass
