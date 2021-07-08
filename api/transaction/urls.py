#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 08/07/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import validate_document

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   Document Version validation
    # ------------------------------------------------------------------------------------------------------------------
    path('transaction/validate-version/', validate_document, name='document-version-validation'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
