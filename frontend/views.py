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
from api.transaction.utils.integration import validate_document_version
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
        auto_download = request.GET.get('download', False)
        if queryset.filter(id=version.document.id).exists():  # security check
            is_last = version == \
                      DocumentVersion.objects.filter(document=version.document).order_by('-creation_timestamp')[0]
            file_name = version.file_resource.name
            validation_flag, tx_address = validate_document_version(version)
            return render(request, 'document_version_detail_page.html',
                          {'version': version, 'is_last': is_last, 'file_name': file_name,
                           'auto_download': auto_download is not False, 'validation_flag': validation_flag,
                           'tx_address': tx_address})
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
