#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 22/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views

from frontend import views

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   Frontend urls
    # ------------------------------------------------------------------------------------------------------------------
    path('', views.document_list_view, name='document-list'),
    path('document_detail/', views.document_versions_list_view, name='document-versions'),
    path('document_version_detail/', views.document_version_detail_view, name='version-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
