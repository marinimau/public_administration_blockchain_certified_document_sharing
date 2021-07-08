#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

import sys

from django.apps import AppConfig


class DocumentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.document'

    def ready(self):
        if 'test' not in sys.argv:
            import api.document.signals