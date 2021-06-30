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

from .views import DocumentsViewSet, PermissionViewSet, FavoriteViewSet, DocumentsVersionViewSet

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   Document Views
    # ------------------------------------------------------------------------------------------------------------------
    path('document/', DocumentsViewSet.as_view({'get': 'list', 'post': 'create'}), name='document-list'),
    path('document/<int:pk>', DocumentsViewSet.as_view({'get': 'retrieve', 'put': 'partial_update'}),
         name='document-detail'),
    # ------------------------------------------------------------------------------------------------------------------
    #   Document Versions Views
    # ------------------------------------------------------------------------------------------------------------------
    path('document/<document_id>/versions/', DocumentsVersionViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='document-version-list'),
    path('document/<document_id>/versions/<int:pk>', DocumentsVersionViewSet.as_view({'get': 'retrieve'}),
         name='document-version-detail'),
    # ------------------------------------------------------------------------------------------------------------------
    #   Document Permissions Views
    # ------------------------------------------------------------------------------------------------------------------
    path('permission/', PermissionViewSet.as_view({'get': 'list', 'post': 'create'}), name='permission-list'),
    path('permission/<int:pk>', PermissionViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
         name='permission-detail'),
    # ------------------------------------------------------------------------------------------------------------------
    #   Favorite document Views
    # ------------------------------------------------------------------------------------------------------------------
    path('my_favorites/', FavoriteViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('my_favorites/<int:pk>', FavoriteViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
