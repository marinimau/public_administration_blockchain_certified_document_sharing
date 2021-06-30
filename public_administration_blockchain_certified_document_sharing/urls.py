"""public_administration_blockchain_certified_document_sharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

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
    #   frontend urls
    # ------------------------------------------------------------------------------------------------------------------
    path('', include('frontend.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
