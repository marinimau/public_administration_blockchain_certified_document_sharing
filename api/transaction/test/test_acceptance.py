#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from .abstract_transaction_test import TransactionTestAbstract


class TransactionTestAcceptance(TransactionTestAbstract):
    """
    Transaction test acceptance class
    """

    def test_validate_file(self):
        """
        Test validate document version file (ok)
        """
        pass

    def test_validate_file_fail(self):
        """
        Test validate document version file (fail)
        """
        pass


