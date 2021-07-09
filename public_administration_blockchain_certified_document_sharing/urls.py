#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view

apiurls = [

]

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   admin urls
    # ------------------------------------------------------------------------------------------------------------------
    path('admin/', admin.site.urls),
    # ------------------------------------------------------------------------------------------------------------------
    #   auth urls
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/auth/token/', obtain_auth_token, name='api_token_auth'),
    # ------------------------------------------------------------------------------------------------------------------
    #   document urls
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/', include('api.document.urls')),
    # ------------------------------------------------------------------------------------------------------------------
    #   transaction urls
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/', include('api.transaction.urls')),
    # ------------------------------------------------------------------------------------------------------------------
    #   frontend urls
    # ------------------------------------------------------------------------------------------------------------------
    path('', include('frontend.urls')),
    # ------------------------------------------------------------------------------------------------------------------
    #   documentation urls
    # ------------------------------------------------------------------------------------------------------------------
    path('documentation/schema/', get_schema_view(
        title=settings.PROJECT_INFO["NAME"],
        description=settings.PROJECT_INFO["DESCRIPTION"],
        version=settings.PROJECT_INFO["VERSION"],
    ), name='openapi-schema'),
    path('documentation/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='documentation'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
