#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 21/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.contrib import admin

from .models import DocumentSC, DocumentVersionTransaction

admin.site.register(DocumentSC)
admin.site.register(DocumentVersionTransaction)
