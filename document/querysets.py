#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 20/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.db.models import Q

from document.models import Document, Permission
from user.models import PaOperator, Citizen


def document_queryset(caller):
    """
    Get only documents of the same public authority
    :return:
    """
    if caller.request.user is not None:
        # is authenticated
        if PaOperator.check_if_exists(caller.request.user.username):
            # is an operator
            operator = PaOperator.objects.get(username=caller.request.user.username)
            return Document.objects.filter(
                Q(author__public_authority=operator.public_authority) | Q(require_permission=False))
        else:
            if Citizen.check_if_exists_username(username=caller.request.user.username):
                # is a citizen
                citizen = Citizen.objects.get(username=caller.request.user.username)
                filtered_permissions = Permission.objects.filter(citizen=citizen)
                return Document.objects.filter(
                    Q(id__in=[permission.document.id for permission in filtered_permissions]) | Q(
                        require_permission=False))
    return Document.objects.filter(require_permission=False)

