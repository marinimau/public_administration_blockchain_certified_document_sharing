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

from django.db import models
from django.utils.timezone import now

from api.user.models import PaOperator, Citizen


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document
#
# ----------------------------------------------------------------------------------------------------------------------

class Document(models.Model):
    """
    Document model
    It represent a container of Document version.
    At the Document model are associated document title and description, favorites and view permissions
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, null=False)
    description = models.TextField(null=True, max_length=500)
    author = models.ForeignKey(PaOperator, null=False, on_delete=models.RESTRICT)
    require_permission = models.BooleanField(null=False, default=True)

    def __str__(self):
        """
        To string method
        :return: the document id and title
        """
        return str(self.id) + " - " + self.title


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentVersion(models.Model):
    """
    Document Version model
    It specifies a version for the given document
    Version contains a file resource and a timestamp
    Author of the version may be different from document author
    """

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(PaOperator, null=False, on_delete=models.RESTRICT)
    creation_timestamp = models.DateTimeField(null=False, default=now)
    file_resource = models.FileField(null=False)
    document = models.ForeignKey(Document, null=False, on_delete=models.RESTRICT)

    class Meta:
        unique_together = (('creation_timestamp', 'document'),)

    indexes = [
        models.Index(fields=['creation_timestamp', ]),
    ]

    def __str__(self):
        """
        To string method
        :return: the document id and timestamp
        """
        return str(self.document.id) + " - " + str(self.creation_timestamp)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Permission
#
# ----------------------------------------------------------------------------------------------------------------------

class Permission(models.Model):
    """
    Permission
    It represent the view permission for a given document and a given citizen
    """

    id = models.AutoField(primary_key=True)
    citizen = models.ForeignKey(Citizen, null=False, on_delete=models.RESTRICT)
    document = models.ForeignKey(Document, null=False, on_delete=models.RESTRICT)

    class Meta:
        unique_together = (('citizen', 'document'),)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Favorite
#
# ----------------------------------------------------------------------------------------------------------------------

class Favorite(models.Model):
    """
    Favorite
    It represent the favorite document of a User
    """

    id = models.AutoField(primary_key=True)
    citizen = models.ForeignKey(Citizen, null=False, on_delete=models.RESTRICT)
    document = models.ForeignKey(Document, null=False, on_delete=models.RESTRICT)

    class Meta:
        unique_together = (('citizen', 'document'),)
