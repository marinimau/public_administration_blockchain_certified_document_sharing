#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from .eng.generic_messages import messages as generic_messages
from .eng.document_messages import messages as document_messages
from .eng.transaction_messages import messages as transaction_messages


def get_generic_messages():
    """
    Get the generic messages
    :return: a dict with the generic messages
    """
    return dict(generic_messages)


def get_document_messages():
    """
    Get the document app's messages
    :return: a dict with the document app's messages
    """
    return dict(document_messages)


def get_transaction_messages():
    """
    Get the transaction app's messages
    :return: a dict with the transaction app's messages
    """
    return dict(transaction_messages)

