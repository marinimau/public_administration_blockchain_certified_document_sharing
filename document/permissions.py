#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import permissions

from user.models import PaOperator, Citizen
from .models import Permission


class DocumentListPermissions(permissions.BasePermission):
    """
    Custom permission to document list
    """

    def has_permission(self, request, view):
        return request.user in PaOperator.objects.all()


class DocumentItemPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            isOperator = request.user is not None and PaOperator.objects.filter(username=request.user.username).exists()
            citizen = Citizen.objects.get(username=request.user.username)
            return not obj.require_permission or isOperator or Permission.check_permissions(citizen, obj)
        return False
