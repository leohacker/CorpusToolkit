#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2013, Leo Jiang
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

# Author: Leo Jiang <leo.jiang.dev@gmail.com>

# pylint: disable=I0011,C0301,C0103,R0902,E0202

"""
BiText2TMX converter.

Usage:
bitext2tmx
"""

from datetime import datetime
import errno
import os
import sys

import codecs
from xml.sax import saxutils

from corpustoolkit.language_code import LanguageCode

def main(argv):
    """main function: handle the arguments."""

    num_args = 2
    if len(argv) != num_args :
        print >> sys.stderr, "Too few/many arguments. Expected {num_args}".format(num_args=num_args)
        sys.exit(errno.EINVAL)

    filepath = os.path.expanduser(argv[1])
    filepath = os.path.abspath(filepath)

    validateFilepath(filepath)
    # TODO: check the content of the input bitext file.
    validateContent(filepath)
    bi2tmx(filepath)

def validateFilepath(filepath):
    """Check whether the filepath is valid."""

    if not os.path.exists(filepath):
        print >> sys.stderr, "File not exists: " + filepath
        sys.exit(errno.ENOENT)

    if not os.path.isfile(filepath):
        print >> sys.stderr, "Please specify a bitext file as input."
        sys.exit(errno.ENOENT)

    namelist = os.path.basename(filepath).split('.')
    if len(namelist) != 3:
        print >> sys.stderr, "The input bitext file should be named like 'resource.en-zh.bitext'."
        sys.exit(errno.ENOENT)

    if namelist[2] != "bitext":
        print >> sys.stderr, "The input bitext file should be named like 'resource.en-zh.bitext'."
        sys.exit(errno.ENOENT)

    langpair = namelist[1]

    if (len(langpair) != 5) and (langpair[2] != '-'):
        print >> sys.stderr, "Invalid language pairs. Should be in form of 'en-zh'."
        sys.exit(errno.ENOENT)

    source_lang = langpair.split('-')[0]
    target_lang = langpair.split('-')[1]

    if not LanguageCode(source_lang).isValid or not LanguageCode(target_lang).isValid:
        print >> sys.stderr, "Invalid language ID."
        sys.exit(errno.EINVAL)

def valdiateContent(filepath):
    pass

def bi2tmx(filepath):
    """convert the bitext file to tmx file."""

    dirpath = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    namelist = filename.split('.')
    namestem = namelist[0]
    langpair = namelist[1]

    source_lang = LanguageCode(langpair.split('-')[0])
    target_lang = LanguageCode(langpair.split('-')[1])
    suffix = namelist[2]

    tmxfilename = namestem + "." + suffix + ".tmx"
    tmxfilename = os.path.join(dirpath, tmxfilename)

    bitext_fp = codecs.open(filepath, 'r', encoding="UTF-8")
    tmx_fp = codecs.open(tmxfilename, 'w', encoding="UTF-8")

    tmx_head = """<?xml version="1.0" encoding="UTF-8"?>
<tmx version="1.4">
    <header creationtool="bitext2tmx" creationtoolversion="0.2"
    datatype="PlainText" segtype="sentence" adminlang="en-US"
    srclang="{src}" creationdate="{date}">
    </header>
    <body>""".format(src=source_lang.xx_dash_xx(), date=datetime.now().strftime("%Y%m%dT%H%M%SZ"))

    tmx_fp.write(tmx_head+ os.linesep)

    tu_begin         = '        <tu srclang="{}">'.format(source_lang.TMX_form())
    tuv_source_begin = '            <tuv xml:lang="{}">'.format(source_lang.TMX_form())
    tuv_source_end   = '            </tuv>'
    tuv_target_begin = '            <tuv xml:lang="{}">'.format(target_lang.TMX_form())
    tuv_target_end   = '            </tuv>'
    tu_end           = '        </tu>'

    for line in bitext_fp:
        [source, target] = line.split(u'\t')
        source = source.strip()
        target = target.strip()
        seg_source   = "            <seg>" + saxutils.escape(source)+ "</seg>"
        seg_target   = "            <seg>" + saxutils.escape(target) + "</seg>"

        tmx_fp.write(tu_begin + os.linesep)
        tmx_fp.write(tuv_source_begin + os.linesep)
        tmx_fp.write(seg_source + os.linesep)
        tmx_fp.write(tuv_source_end + os.linesep)
        tmx_fp.write(tuv_target_begin + os.linesep)
        tmx_fp.write(seg_target + os.linesep)
        tmx_fp.write(tuv_target_end + os.linesep)
        tmx_fp.write(tu_end + os.linesep )

    tmx_body_tail = '    </body>'
    tmx_tail = '</tmx>'
    tmx_fp.write(tmx_body_tail + os.linesep)
    tmx_fp.write(tmx_tail + os.linesep)

    bitext_fp.close()
    tmx_fp.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
