#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 19/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#


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

    def __str__(self):
        """
        To string method
        :return: A sting (operator code, wallet address)
        """
        return str(self.operator_code) + " " + str(self.bc_address)

    @staticmethod
    def check_if_exists(username):
        """
        Return true if exists an operator with the given username, false otherwise
        :param username: the username
        :return: true if exists an operator with the given username, false otherwise
        """
        return PaOperator.objects.filter(username=username).exists()


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

    def __str__(self):
        """
        To string method
        :return: the CF of the citizen
        """
        return str(self.cf)

    @staticmethod
    def check_if_exists(cf):
        """
        Given the CF returns true if citizen exists, false otherwise
        :param cf:
        :return: true if citizen exists, false otherwise
        """
        return Citizen.objects.filter(cf=cf).exists()

    @staticmethod
    def check_if_exists_username(username):
        """
        Given the CF returns true if citizen exists, false otherwise
        :param username: the username
        :return: true if citizen exists, false otherwise
        """
        return Citizen.objects.filter(username=username).exists()
