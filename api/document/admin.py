#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.contrib import admin

from .models import Document, DocumentVersion, Permission, Favorite

admin.site.register(Document)
admin.site.register(DocumentVersion)
admin.site.register(Permission)
admin.site.register(Favorite)