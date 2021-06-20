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


class DocumentItemPermissions(permissions.BasePermission):
    """
    Custom permission for Document model
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


class DocumentVersionPermissions(DocumentItemPermissions):
    """
    Custom permission for document version model
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return super(DocumentVersionPermissions, self).has_object_permission(request, view, obj.document)


def check_operator(username, document, write_request, write_accepted):
    """
    Return True if the username is associated to an operator an he has works on the same public authority of the author
    of document
    :param username: the username
    :param document: the Document
    :param write_request: a flag that indicates if the request is a write request
    :param write_request: a flag that indicates if the request is a write request
    :param write_accepted:a flag that indicate if the object allow a write request
    :return:
    """
    exists = PaOperator.objects.filter(username=username).exists()
    if exists:
        operator = PaOperator.objects.get(username=username)
        if write_request:
            if write_accepted:
                return operator.public_authority == document.author.public_authority
            return False
        else:
            return not document.require_permission
    return False
