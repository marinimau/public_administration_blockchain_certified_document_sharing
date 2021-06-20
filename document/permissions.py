#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from user.models import PaOperator, Citizen
from .models import Permission, Document


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


class IsOwner(permissions.BasePermission):
    """
    Custom permission: return true if is a Citizen is Owner of an object
    """

    def has_object_permission(self, request, view, obj):
        return request.user is not None and Citizen.objects.filter(
            username=request.user.username).exists() and obj.citizen.username == request.user.username


class IsOperatorSamePublicAuthority(permissions.BasePermission):
    """
    Custom write permissions: only an operator of the same PA can write
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            exists = request.user is not None and PaOperator.check_if_exists(request.user.username)
            if exists:
                operator = PaOperator.objects.get(username=request.user.username)
                return obj.author.public_authority == operator.public_authority
        return False