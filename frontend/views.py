#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 22/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from rest_framework.status import HTTP_404_NOT_FOUND

from api.document.models import DocumentVersion, Favorite, Document
from api.document.querysets import document_queryset

# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------
from api.user.models import Citizen


def document_list_view(request):
    """
    Document list page
    :param request: the request
    :return: the page
    """
    document_list = document_queryset(request)  # api.document.queryset is permission filtered
    return render(request, 'document_list_page.html', {'documents': document_list})


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Versions
#
# ----------------------------------------------------------------------------------------------------------------------

def document_versions_list_view(request, document_id):
    """
    Document detail and version list page
    :param request: the request
    :param document_id: the id of the document
    :return: the page
    """
    queryset = document_queryset(request)  # api.document.queryset is permission filtered
    exists = queryset.filter(id=document_id).exists()
    if exists:
        document = queryset.get(id=document_id)
        versions = DocumentVersion.objects.filter(document=document).order_by('-creation_timestamp')
        is_favorite = Favorite.objects.filter(document__id=document_id,
                                              citizen__username=request.user.username).exists()
        return render(request, 'document_detail_and_version_list.html',
                      {'document': document, 'versions': versions, 'is_favorite': is_favorite})
    return handler404(request)


def document_version_detail_view(request, version_id):
    """
    Version detail page
    :param request: the request
    :param version_id: the id of the document version
    :return: the page
    """
    queryset = document_queryset(request)  # api.document.queryset is permission filtered
    exists = DocumentVersion.objects.filter(id=version_id).exists()
    if exists:
        version = DocumentVersion.objects.get(id=version_id)
        if queryset.filter(id=version.document.id).exists():  # security check
            is_last = version == \
                      DocumentVersion.objects.filter(document=version.document).order_by('-creation_timestamp')[0]
            file_name = version.file_resource.name
            return render(request, 'document_version_detail_page.html',
                          {'version': version, 'is_last': is_last, 'file_name': file_name})
    return handler404(request)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Favorites
#
# ----------------------------------------------------------------------------------------------------------------------

def favorites_list_view(request):
    """
   Favorite list page
   :param request: the request
   :return: the page
   """
    if request.user is not None:
        favorites = Favorite.objects.filter(citizen__username=request.user.username)
        document_list = document_queryset(request).filter(id__in=[f.document.id for f in favorites])
        return render(request, 'document_list_page.html', {'documents': document_list})
    return handler404(request)


@login_required
@require_POST
def handle_favorite(request):
    """
    Add / remove a document to favorite
    :param request: the request
    :return: the favorite status
    """
    document_id = request.POST.get('document_id', None)
    if request.method == 'POST' and Citizen.objects.filter(
            username=request.user.username).exists() and Document.objects.filter(id=document_id).exists():
        if not Favorite.objects.filter(citizen__username=request.user.username, document__id=document_id).exists():
            Favorite.objects.create(citizen=Citizen.objects.get(username=request.user.username),
                                    document=Document.objects.get(id=document_id))
            return JsonResponse({'is_favorite': True})
        else:
            Favorite.objects.filter(citizen__username=request.user.username, document__id=document_id).delete()
            return JsonResponse({'is_favorite': False})


# ----------------------------------------------------------------------------------------------------------------------
#
#   Error 404
#
# ----------------------------------------------------------------------------------------------------------------------

def handler404(request):
    """
    A custom 404 error page for the documents
    :param request: the request
    :return: the render of the 404 error page
    """
    return render(request, '404.html', {}, status=HTTP_404_NOT_FOUND)
