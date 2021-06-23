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

from api.document.models import DocumentVersion
from api.document.querysets import document_queryset


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

def document_list_view(request):
    document_list = document_queryset(request) # api.document.queryset is permission filtered
    return render(request, 'document_list_page.html', {'documents': document_list, 'len_documents': len(document_list)})


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

def document_versions_list_view(request):
    document_id = request.POST.get("document_id")
    queryset = document_queryset(request)  # api.document.queryset is permission filtered
    exists = queryset.filter(id=document_id).exists()
    if exists:
        document = queryset.get(id=document_id)
        versions = DocumentVersion.objects.filter(document=document).order_by('-creation_timestamp')
        return render(request, 'document_detail_and_version_list.html', {'document': document, 'versions': versions})
    return error_404(request)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Versions
#
# ----------------------------------------------------------------------------------------------------------------------

def document_version_detail_view(request):
    # document_id = request.POST.get("document_id")
    queryset = document_queryset(request)  # api.document.queryset is permission filtered
    exists = True
    if exists:
        version = 0
        return render(request, 'document_version_detail_page.html', {'version': version})
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
