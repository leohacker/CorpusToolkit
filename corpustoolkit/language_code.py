# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2012, 2013 Leo Jiang
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author:   Leo Jiang <leo.jiang.dev@gmail.com>

# pylint: disable=I0011,C0301,C0103

"""
LanguageCode Module
"""

import locale


class LanguageCode(object):
    """Language code class.

    Currently constructor accept three forms of language code as parameter: xx, xx_XX,
    xx-XX, case insensitive. And we can get kinds of forms of language code. So we can
    convert between the forms of language code.

    """

    def __init__(self, langcode):
        """LanguageCode Constructor.

        Accept three forms of language code: xx, xx_XX, xx-XX, case insensitive.
        Also accept the form of xx_xx.encoding, the encoding part will be wiped off.

        """
        # Wipe off the encoding part and normalize the form to locale acceptable.
        langcode = langcode.split('.')[0].replace('-', '_')

        # locale.normalize return the xx_XX.encoding form of locale.
        # Only the legal language code can be recognized and suffixed with encoding.
        # Otherwise return the same string.
        if langcode == locale.normalize(langcode):
            self._langcode = None
        else:
            self._langcode = locale.normalize(langcode).split('.')[0]
            self._lang = self._langcode.split('_')[0]
            self._country = self._langcode.split('_')[1]

    def isValid(self):
        """Return True if is a valid language code."""
        return True if self._langcode is not None else False

    def xx(self):
        """return lowercase version of two chars form."""
        return self._lang.lower()

    def XX(self):
        """return uppercase version of two chars form."""
        return self._lang.upper()

    def xx_xx(self):
        """return xx_xx"""
        return '_'.join([self._lang.lower(), self._country.lower()])

    def xx_XX(self):
        """return xx_XX form of language code."""
        return '_'.join([self._lang.lower(), self._country.upper()])

    def TMX_form(self):
        """return TMX form (xx-XX) of language code."""
        return '-'.join([self._lang.lower(), self._country.upper()])

    def xx_dash_xx(self):
        """return xx-xx form of language code."""
        return '-'.join([self._lang.lower(), self._country.lower()])

    def XX_dash_XX(self):
        """return XX-XX form of language code."""
        return '-'.join([self._lang.upper(), self._country.upper()])
