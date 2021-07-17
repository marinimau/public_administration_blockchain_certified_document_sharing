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
from django.contrib.auth.models import User
from gnosis.eth.django.models import EthereumAddressField


# ----------------------------------------------------------------------------------------------------------------------
#
#   PublicAuthority
#
# ----------------------------------------------------------------------------------------------------------------------

class PublicAuthority(models.Model):
    """
    Public Authority model:
    It represents the public authority to which the public operator belongs
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=40, null=False)


# ----------------------------------------------------------------------------------------------------------------------
#
#   PaOperator
#
# ----------------------------------------------------------------------------------------------------------------------

class PaOperator(User):
    """
    PaOperator model:
    It represents the staff user. It is a subclass of the standard user.
    PaOperator can create document and certificate them. To accomplish this task it need a Wallet address and the
    secret token.
    """

    operator_code = models.CharField(unique=True, max_length=10, null=False)
    public_authority = models.ForeignKey(PublicAuthority, null=False, on_delete=models.CASCADE)
    bc_address = EthereumAddressField(null=False)
    bc_secret_key = models.CharField(max_length=200, null=False)

    class Meta:
        verbose_name = 'Pa Operator'

    def __str__(self):
        """
        To string method
        :return: A sting (operator code, wallet address)
        """
        return str(self.operator_code) + " " + str(self.bc_address)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Citizen
#
# ----------------------------------------------------------------------------------------------------------------------

class Citizen(User):
    """
    Citizen model:
    It represent the italian citizen. It is a subclass of the standard user.
    Citizen can only view / download document, add the to his favorites and view the versions.
    """

    class Regions(models.TextChoices):
        """
            Regions enumeration
            Citizens belong to a region
        """
        ABR = 'ABRUZZO'
        BAS = 'BASILICATA'
        CAL = 'CALABRIA'
        CAM = 'CAMPANIA'
        EMR = 'EMILIA-ROMAGNA'
        FVG = 'FRIULI-VENEZIA-GIULIA'
        LAZ = 'LAZIO'
        MAR = 'MARCHE'
        MOL = 'MOLISE'
        PAB = 'PROVINCIA-AUTONOMA-BOLZANO'
        PAT = 'PROVINCIA-AUTONOMA-TRENTO'
        PMT = 'PIEMONTE'
        PUG = 'PUGLIA'
        SAR = 'SARDEGNA'
        SIC = 'SICILIA'
        TOS = 'TOSCANA'
        UMB = 'UMBRIA'
        VDA = 'VALLE-D-AOSTA'
        VEN = 'VENETO'

    cf = models.CharField(unique=True, max_length=16, null=False)
    region = models.CharField(choices=Regions.choices, max_length=30, null=False)

    class Meta:
        verbose_name = 'Citizen'

    def __str__(self):
        """
        To string method
        :return: the CF of the citizen
        """
        return str(self.cf)


