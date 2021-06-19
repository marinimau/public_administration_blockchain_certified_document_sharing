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


class IsPaOperator(permissions.BasePermission):
    """
    Custom permission: return true if is a PA operator
    """

    def has_permission(self, request, view):
        return request.user is not None and PaOperator.objects.filter(username=request.user.username).exists()


class IsCitizen(permissions.BasePermission):
    """
    Custom permission: return true if is a Citizen
    """

    def has_permission(self, request, view):
        return request.user is not None and Citizen.objects.filter(username=request.user.username).exists()


class DocumentItemPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        is_operator = request.user is not None and PaOperator.objects.filter(username=request.user.username).exists()
        is_citizen = request.user is not None and Citizen.objects.filter(username=request.user.username).exists()
        if request.method == 'GET':
            is_authorized_citizen = False
            if is_citizen:
                citizen = Citizen.objects.get(username=request.user.username)
                is_authorized_citizen = Permission.check_permissions(citizen, obj)
            return not obj.require_permission or is_operator or is_authorized_citizen
        if request.method == 'UPDATE' or request.method == 'PUT':
            return is_operator
        return False
