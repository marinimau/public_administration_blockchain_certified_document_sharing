"""
This software is distributed under MIT/X11 license

Copyright (c) 2021 Mauro Marini - University of Cagliari

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

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
    path('my_favorites/', FavoriteViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite-list'),
    path('my_favorites/<int:pk>', FavoriteViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
         name='favorite-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
