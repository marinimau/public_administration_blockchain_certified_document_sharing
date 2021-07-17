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

from .eng.generic_messages import messages as generic_messages
from .eng.document_messages import messages as document_messages
from .eng.transaction_messages import messages as transaction_messages


def get_generic_messages():
    """
    Get the generic messages
    :return: a dict with the generic messages
    """
    return dict(generic_messages)


def get_document_messages():
    """
    Get the document app's messages
    :return: a dict with the document app's messages
    """
    return dict(document_messages)


def get_transaction_messages():
    """
    Get the transaction app's messages
    :return: a dict with the transaction app's messages
    """
    return dict(transaction_messages)

