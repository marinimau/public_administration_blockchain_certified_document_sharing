#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 22/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.shortcuts import render
from rest_framework.status import HTTP_404_NOT_FOUND

from api.document.models import DocumentVersion, Favorite
from api.document.querysets import document_queryset


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

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
        return render(request, 'document_detail_and_version_list.html', {'document': document, 'versions': versions})
    return error_404(request)


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
    return error_404(request)


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
    return error_404(request)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Error 404
#
# ----------------------------------------------------------------------------------------------------------------------

def error_404(request):
    """
    A custom 404 error page for the documents
    :param request: the request
    :return: the render of the 404 error page
    """
    return render(request, '404.html', {}, status=HTTP_404_NOT_FOUND)
