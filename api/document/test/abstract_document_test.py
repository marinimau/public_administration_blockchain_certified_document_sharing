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

from rest_framework.test import APITestCase

from api.document.models import Document, Permission, Favorite, DocumentVersion
from api.user.models import PublicAuthority, PaOperator, Citizen


class DocumentTestAbstract(APITestCase):
    """
    Test for document app
    """
    RANGE_MAX = 3
    RANGE_MAX_DOCUMENTS = 5
    RANGE_MAX_DOCUMENT_VERSIONS = 8
    RANGE_PERMISSIONS_MAX = RANGE_MAX_DOCUMENTS - 1

    class Meta:
        abstract = True

    @classmethod
    def setUpTestData(cls):
        """
        Set-up the data for the test
        :return:
        """
        # 1. Setup Public Authorities
        cls.public_authorities = [PublicAuthority.objects.create(name=('Authority' + str(i))) for i in
                                  range(cls.RANGE_MAX)]

        # 2. Setup PA operators
        cls.pa_operators = [PaOperator.objects.create(
            username=('operator' + str(i)),
            email=('operator' + str(i) + '@operators.com'),
            password='test',
            is_active=True,
            operator_code=('OP' + str(i)),
            public_authority=cls.public_authorities[i],
            bc_address='0x000000000000000000000000000000000000000' + str(i),
            bc_secret_key='secret'
        ) for i in range(cls.RANGE_MAX)]
        [pa.set_password('PaOperator123.') for pa in cls.pa_operators]

        # 2. Setup Citizens
        cls.citizens = [Citizen.objects.create(
            username=('citizen' + str(i)),
            email=('citizen' + str(i) + '@citizen.com'),
            password='test',
            is_active=True,
            cf=('ctzctz00c00c000' + str(i)),
            region=Citizen.Regions.SIC
        ) for i in range(cls.RANGE_MAX)]
        [c.set_password('Citizen123.') for c in cls.citizens]

        # 3. Setup Documents
        cls.documents = [Document.objects.create(
            title=('Document ' + str(i)),
            description=('This is the description of the document ' + str(i)),
            author=cls.pa_operators[0],
            require_permission=(True if i % cls.RANGE_MAX == 0 else False)
        ) for i in range(cls.RANGE_MAX_DOCUMENTS)]

        # 4. Setup Document Versions
        cls.documents_versions = [DocumentVersion.objects.create(
            author=cls.pa_operators[0],
            document=cls.documents[0],
        ) for _ in range(cls.RANGE_MAX_DOCUMENT_VERSIONS)]

        # 5. Setup Permissions
        cls.permissions = [Permission.objects.create(
            citizen=cls.citizens[0],
            document=cls.documents[i]
        ) for i in range(cls.RANGE_PERMISSIONS_MAX)]

        # 6. Setup Favorites
        cls.favorites = [Favorite.objects.create(
            citizen=cls.citizens[0],
            document=cls.documents[i]
        ) for i in range(cls.RANGE_MAX_DOCUMENTS - 1)]

    def test_check_created_data(self):
        """
        Check the data created by setUpTestData
        :return:
        """
        self.assertEqual(len(self.public_authorities), self.RANGE_MAX)
        self.assertEqual(len(self.pa_operators), self.RANGE_MAX)
        self.assertEqual(len(self.citizens), self.RANGE_MAX)
        self.assertEqual(len(self.documents), self.RANGE_MAX_DOCUMENTS)
        self.assertEqual(len(self.documents_versions), self.RANGE_MAX_DOCUMENT_VERSIONS)
        self.assertEqual(len(self.permissions), self.RANGE_MAX_DOCUMENTS - 1)
        self.assertEqual(len(self.favorites), self.RANGE_MAX_DOCUMENTS - 1)
