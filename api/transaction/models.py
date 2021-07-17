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
    creation_timestamp = models.DateTimeField(null=False, default=now)

    class Meta:
        abstract = True

    def __str__(self):
        """
        To string method
        :return: The address of the transaction
        """
        return str(self.id)


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
    document = models.OneToOneField(Document, on_delete=models.RESTRICT, related_name='document_sc', null=False)


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
    document_version = models.OneToOneField(DocumentVersion, on_delete=models.RESTRICT,
                                            related_name='version_transaction', null=False)
    download_url = models.URLField(null=False)
