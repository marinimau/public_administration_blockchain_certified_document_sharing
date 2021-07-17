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

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import Document
from api.user.models import PaOperator, Citizen


# ----------------------------------------------------------------------------------------------------------------------
#
#   Generic
#
# ----------------------------------------------------------------------------------------------------------------------

class IsPaOperator(permissions.BasePermission):
    """
    Custom permission: return true if PA operator
    """

    def has_permission(self, request, view):
        return request.user is not None and PaOperator.objects.filter(username=request.user.username).exists()


class IsCitizen(permissions.BasePermission):
    """
    Custom permission: return true if Citizen
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


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentPermissions(permissions.BasePermission):
    """
    Custom permissions for model Document
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return permissions.AllowAny
        else:
            return request.user is not None and PaOperator.objects.filter(username=request.user.username).exists()

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False
        if request.method in SAFE_METHODS:
            return permissions.AllowAny
        else:
            exists = request.user is not None and PaOperator.objects.filter(username=request.user.username).exists()
            if exists:
                operator = PaOperator.objects.get(username=request.user.username)
                return obj.author.public_authority == operator.public_authority
        return False


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentVersionPermission(permissions.BasePermission):
    """
    Custom permissions for document version
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return permissions.AllowAny
        else:
            exists = request.user is not None and PaOperator.objects.filter(username=request.user.username).exists()
            if exists:
                operator = PaOperator.objects.get(username=request.user.username)
                document_id = request.resolver_match.kwargs.get('document_id')
                if Document.objects.filter(id=document_id).exists():
                    obj = Document.objects.get(id=document_id)
                    return obj.author.public_authority == operator.public_authority
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            return False
