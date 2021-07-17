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

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Document, DocumentVersion
from api.transaction.utils.integration import create_document_contract, create_document_version_transaction


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

@receiver(post_save, sender=Document)
def create_document_sc(sender, instance, created, *args, **kwargs):
    """
    Pre-save for document model, we use it to create the document sc
    :param sender: the sender
    :param instance: The document instance
    :param created: a flag that indicate if obj is created
    :return:
    """
    if created:
        create_document_contract(document=instance)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version
#
# ----------------------------------------------------------------------------------------------------------------------

@receiver(post_save, sender=DocumentVersion)
def create_document_sc(sender, instance, created, *args, **kwargs):
    """
    Pre-save for document version model, we use it to create the document version transaction in the document sc
    :param created: a flag that indicate if obj is created
    :param sender: the sender
    :param instance: The document version instance
    :return:
    """
    if created:
        create_document_version_transaction(document_version=instance)
