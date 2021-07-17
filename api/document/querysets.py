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

from django.db.models import Q

from .models import Document, Permission, DocumentVersion
from api.user.models import PaOperator, Citizen


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

def document_queryset(request):
    """
    Get document with read permissions
    :return:
    """
    if request.user is not None:
        # is authenticated
        if PaOperator.objects.filter(username=request.user.username).exists():
            # is an operator
            operator = PaOperator.objects.get(username=request.user.username)
            return Document.objects.filter(
                Q(author__public_authority=operator.public_authority) | Q(require_permission=False))
        else:
            if Citizen.objects.filter(username=request.user.username).exists():
                # is a citizen
                citizen = Citizen.objects.get(username=request.user.username)
                filtered_permissions = Permission.objects.filter(citizen=citizen)
                return Document.objects.filter(
                    Q(id__in=[permission.document.id for permission in filtered_permissions]) | Q(
                        require_permission=False))
    return Document.objects.filter(require_permission=False)


def document_write_queryset(request):
    """
    Get document with read permissions
    :return:
    """
    if request.user is not None:
        # is authenticated
        if PaOperator.objects.filter(username=request.user.username).exists():
            # is an operator
            operator = PaOperator.objects.get(username=request.user.username)
            return Document.objects.filter(author__public_authority=operator.public_authority)
    return Document.objects.none()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version
#
# ----------------------------------------------------------------------------------------------------------------------

def document_version_queryset(caller):
    """
    Get the versions associated to the given document
    :return:
    """
    document_id = caller.kwargs['document_id']
    doc_queryset = document_queryset(caller.request)
    exists_document = doc_queryset.filter(id=document_id).exists()
    if exists_document:
        document = doc_queryset.get(id=document_id)
        return DocumentVersion.objects.filter(document=document)
    return DocumentVersion.objects.none()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Permission
#
# ----------------------------------------------------------------------------------------------------------------------

def permission_all_queryset(caller):
    """
    Get the permissions associated to document of the same public authority of the operator
    :return:
    """
    operator = PaOperator.objects.get(username=caller.request.user.username)
    return Permission.objects.filter(document__author__public_authority=operator.public_authority)
