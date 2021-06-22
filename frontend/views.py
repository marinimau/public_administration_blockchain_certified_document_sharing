#
#   public_administration_blockchain_certified_document_sharing copyright © 2021 - all rights reserved
#   Created at: 22/06/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/public_administration_blockchain_certified_document_sharing
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.shortcuts import render
from rest_framework.status import HTTP_404_NOT_FOUND


# ----------------------------------------------------------------------------------------------------------------------
#
#   Favorite
#
# ----------------------------------------------------------------------------------------------------------------------

def error_404(request):
    """
    A custom 404 error page for the documents
    :param request: the request
    :return: the render of the 404 error page
    """
    return render(request, '404.html', {}, status=HTTP_404_NOT_FOUND)
