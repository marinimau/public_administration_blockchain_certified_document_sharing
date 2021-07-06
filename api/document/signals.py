#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 05/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Document, DocumentVersion
from ..transaction.integration import create_document_contract, create_document_version_transaction


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
