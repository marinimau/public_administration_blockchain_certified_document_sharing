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

from .views import DocumentsList, DocumentDetail, PermissionListDocument, PermissionListUser, PermissionCreation, \
    PermissionDetail, FavoriteOfCitizenList, FavoriteDetail

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   Document Views
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/document/', DocumentsList.as_view()),
    path('api/v1/document/<int:pk>', DocumentDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   Document Versions Views
    # ------------------------------------------------------------------------------------------------------------------
    # path('api/v1/documents/<document_id>/versions/', DocumentVersionList.as_view())
    # path('api/v1/documents/<document_id>/versions/<int:pk>', DocumentVersionList.as_view())
    # ------------------------------------------------------------------------------------------------------------------
    #   Document Permissions Views
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/document/<document_id>/view_permissions/', PermissionListDocument.as_view()),
    path('api/v1/citizen/<cf>/view_permissions/', PermissionListUser.as_view()),
    path('api/v1/create_permission/', PermissionCreation.as_view()),
    path('api/v1/permission_detail/<int:pk>', PermissionDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   Favorite document Views
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/my_favorites/', FavoriteOfCitizenList.as_view()),
    path('api/v1/my_favorites/<int:pk>', FavoriteDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
