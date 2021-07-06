#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from gnosis.eth.django.models import EthereumAddressField, HexField
from django.db import models
from django.utils.timezone import now

from api.document.models import Document, DocumentVersion


# ----------------------------------------------------------------------------------------------------------------------
#
#   Abstract Transaction
#
# ----------------------------------------------------------------------------------------------------------------------

class AbstractTransaction(models.Model):
    """
    Abstract Transaction
    This class represent an abstract model of transaction
    DocumentTransaction model and DocumentVersionTransaction model extend this class
    """
    id = models.AutoField(primary_key=True)
    author_address = EthereumAddressField(null=False)
    creation_timestamp = models.DateField(null=False, default=now)

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
#   Document SC
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentSC(AbstractTransaction):
    """
    Document Transaction
    This class represent the model of transaction for Document model
    """
    transaction_address = EthereumAddressField(null=False, unique=True)
    document = models.OneToOneField(Document, on_delete=models.RESTRICT)


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

    transaction_address = HexField(null=False, max_length=500)
    hash_fingerprint = models.CharField(max_length=256, null=False)
    document_version = models.OneToOneField(DocumentVersion, on_delete=models.RESTRICT, null=False)
    download_url = models.URLField(null=False)
