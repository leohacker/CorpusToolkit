#!/usr/bin/env python
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

# Author: Leo Jiang <leo.jiang.dev@gmail.com>

# pylint: disable=I0011,C0301,C0103,R0902,E0202

"""
TMX file parser.

TMX file parser run the expat xml parser tool to extract the translation unit.
For every tu, call the external function to output the translation unit as bitext,
plain text, or into database, etc.
"""

import logging
import os.path
from xml.parsers.expat import ParserCreate
from xml.parsers.expat import ExpatError


class TMXParser(object):
    """TMXParser read a TMX file and extract all translation units.

    The extracted translation unit is passed to a specific output object.
    This output object is created by caller program, then caller program
    can redirect the output to bitext, plain text or database. And the caller
    program can collect the statistic data according own requirement.

    This tmx parser use xml.parsers.expat as xml parser engine.
    """
    def __init__(self):
        # self.aligns is a dictionary, like { "en-US": "first line. second line.",
        #                                     "de-DE": "Germany sentences.",
        #                                     "zh-CN": "Simpilified Chinese sentences" }
        # For any source tuv in tu, it would have only one corresponding translation.
        # For any source tuv in tu, it would have several target translations.
        self.aligns = None

        # The flag 'in_seg' indicate whether current event happens in the middle of paring a seg.
        # Because some tag-like words are embedded in sentence, the parser would get a new start
        # element event.
        # self.seg, keep the text for current <seg> even the embedded tag-like text.
        # self.tuv_lang, the language of current parsed tuv.
        self.in_seg = False
        self.seg = None
        self.tuv_lang = None

        self.output_func = None

        self.parser = ParserCreate()
        self.parser.buffer_text = True
        self.parser.buffer_size = 4096
        self.parser.returns_unicode = True

        self.parser.StartElementHandler = self.start_element_handler
        self.parser.EndElementHandler = self.end_element_handler
        self.parser.CharacterDataHandler = self.char_data_handler


    def set_output_callback(self, func):
        """Set the output callback function."""
        self.output_func = func


    def parse_file(self, filename):
        """Expat parser file function.

        Return 0 if succeed, else return error code.
        """
        # Open the tmx file as file object. Don't specify the encoding.
        # ParseFile only need a file object with read(nbytes) method.
        # So we can use ParseFile read the xml with encoding either UTF-8 or UTF-16.
        try:
            logging.debug("Open the file: {}".format(filename))
            fp = open(filename)
        except IOError as e:
            logging.debug("Failed to open.")
            logging.error(e)
            return e.errno

        # whether success or fail, close the files and quit.
        logging.info("Parsing the TMX file {} ...".format(os.path.basename(filename)))
        try:
            self.parser.ParseFile(fp)
        except ExpatError as e:
            logging.error(e)
            return e.code
        finally:
            fp.close()

        logging.info("Parsing completed.")
        return 0


    def start_element_handler(self, name, attributes):
        """Expat parser callback function."""
        if (self.in_seg):
            attrlist = [ attrname + '=' + '"'+ attributes[attrname] + '"' for attrname in attributes.keys() ]
            attrstr = ' '.join(attrlist)
            tagheader = '<' + name + ' ' + attrstr + '>'
            self.seg += tagheader
        if (name == u"tu"):
            self.aligns = {}
        if (name == u"tuv"):
            self.tuv_lang = attributes["xml:lang"]
        if (name == u"seg"):
            self.seg = u''
            self.in_seg = True


    def end_element_handler(self, name):
        """Expat parser callback function."""
        # write the aligns into database.
        if (name == u"tu"):
            self.output_func(self.aligns)

        # clear the tuv_lang (current language)
        if (name == u"tuv"):
            self.tuv_lang = None

        # end of seg, store the seg text into aligns dictionary.
        if (name == u"seg"):
            self.aligns[self.tuv_lang] = self.seg
            self.in_seg = False
            self.seg = None

        # handle the embedded tag in seg.
        if (self.in_seg):
            tagtail = "</" + name + ">"
            self.seg += tagtail


    def char_data_handler(self, data):
        """Expat parser callback function."""
        if self.in_seg:
            self.seg += data
