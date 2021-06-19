#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import DocumentsList, DocumentDetail

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   Document Views
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/documents/', DocumentsList.as_view()),
    path('api/v1/documents/<int:pk>', DocumentDetail.as_view()),
    # path('api/v1/documents/<document_id>/versions/', DocumentVersionList.as_view())
    # path('api/v1/documents/<document_id>/versions/<int:pk>', DocumentVersionList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
