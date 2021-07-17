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

from contents.messages.get_messages import get_generic_messages
from .models import DocumentSC, DocumentVersionTransaction

generic_messages = get_generic_messages()


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document SC Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentSCSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSC
        fields = ['id', 'transaction_address', 'author_address', 'creation_timestamp', 'document']
        read_only_fields = ['id', 'transaction_address', 'author_address', 'creation_timestamp', 'document']


# ----------------------------------------------------------------------------------------------------------------------
#
#   Document Version Transaction Serializer
#
# ----------------------------------------------------------------------------------------------------------------------

class DocumentVersionTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersionTransaction
        fields = '__all__'
