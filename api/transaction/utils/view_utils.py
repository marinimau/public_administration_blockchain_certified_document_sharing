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

from rest_framework import serializers

from contents.messages.get_messages import get_transaction_messages
from ...document.models import DocumentVersion

transaction_messages = get_transaction_messages()


def validate_version_id(version_id):
    """
    Validate the version id
    :param version_id: the version id
    :return: the version id or an error
    """
    try:
        version_id = int(version_id)
    except ValueError:
        raise serializers.ValidationError(transaction_messages['bad_version_id'])
    if version_id is not None and isinstance(version_id, int) and DocumentVersion.objects.filter(
            id=version_id).exists():
        return version_id
    else:
        raise serializers.ValidationError(transaction_messages['version_not_found'])


def get_validation_description(validation_flag):
    """
    Return the validation description from the validation flag
    :param validation_flag: the validation flag
    :return: the validation description
    """
    if validation_flag == -1:
        return 'ALTERED'
    elif validation_flag == 1:
        return 'VALIDATED'
    else:
        return 'UNAVAILABLE'
