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
