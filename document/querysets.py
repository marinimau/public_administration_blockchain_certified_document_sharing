#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 20/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.db.models import Q

from document.models import Document, Permission, DocumentVersion
from user.models import PaOperator, Citizen


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

def document_queryset(request):
    """
    Get only documents of the same public authority
    :return:
    """
    if request.user is not None:
        # is authenticated
        if PaOperator.check_if_exists(request.user.username):
            # is an operator
            operator = PaOperator.objects.get(username=request.user.username)
            return Document.objects.filter(
                Q(author__public_authority=operator.public_authority) | Q(require_permission=False))
        else:
            if Citizen.check_if_exists_username(username=request.user.username):
                # is a citizen
                citizen = Citizen.objects.get(username=request.user.username)
                filtered_permissions = Permission.objects.filter(citizen=citizen)
                return Document.objects.filter(
                    Q(id__in=[permission.document.id for permission in filtered_permissions]) | Q(
                        require_permission=False))
    return Document.objects.filter(require_permission=False)


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

