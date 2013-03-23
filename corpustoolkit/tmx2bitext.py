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

# pylint: disable=I0011,C0301,C0111,C0103

"""
TMX2BiText Converter

Convert the tmx file or tmx files in a directory into bitext file(s).

Command line syntax::

    Usage: tmx2bitext.py [options] file|directory source_lang target_lang

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o DIR, --output-dir=DIR
                            output directory
      -l FILE, --log=FILE   log file
      -D, --Debug           logging debug message

"""

import codecs
import glob
import logging
import os.path
import sys

from optparse import OptionParser

from corpustoolkit.tmxparser import TMXParser
from corpustoolkit.language_code import LanguageCode


__version__ = 1.0
__years__ = "2013"
__author__ = "Leo Jiang <leo.jiang.dev@gmail.com>"


def main(argv):    # pylint: disable=I0011,W0102
    usage = "Usage: %prog [options] file|directory source_lang target_lang"
    num_args = 3
    version = "%prog {version} (c) {years} {author}".format(version=__version__,
                                                            years=__years__,
                                                            author=__author__
                                                            )
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-o", "--output-dir", metavar="DIR", dest="output_dir",
                      type="string", help="output directory")
    parser.add_option("-l", "--log", metavar="FILE", dest="log",
                      type="string", help="log file")
    parser.add_option("-D", "--Debug", metavar="DEBUG", dest="debug",
                      action="store_true", help="logging debug message", default=False)
    (options, args) = parser.parse_args(argv[1:])
    if len(args) != num_args:
        parser.error("Too few/many arguments. Expected {num_args}".format(num_args=num_args))

    # check the arguments.
    pathname = os.path.abspath(os.path.expanduser(args[0]))
    if not os.path.exists(pathname):
        parser.error("Invalid file or directory: {}".format(args[0]))

    source_lang = LanguageCode(args[1])
    target_lang = LanguageCode(args[2])
    if not source_lang.isValid() or not target_lang.isValid():
        parser.error("Invalid language code.")

    source_lang = source_lang.TMX_form()
    target_lang = target_lang.TMX_form()

    # setup output directory, logging level and log file according to user-specific options.
    if options.output_dir is not None:
        output_dir = os.path.abspath(os.path.expanduser(options.output_dir))
    elif os.path.isdir(pathname):
        output_dir = pathname
    else:
        output_dir = os.path.dirname(pathname)
    if not os.path.exists(output_dir):
        parser.error("Invalid output directory.")

    loglevel = logging.INFO
    if options.debug :
        loglevel = logging.DEBUG

    logging.basicConfig(filename=options.log, level=loglevel, format="%(message)s")

    tmx2bitext = TMX2BiText()
    tmx2bitext.setLangs(source_lang, target_lang)
    tmx2bitext.setOutputDir(output_dir)
    tmx2bitext.setInputFileDir(pathname)
    tmx2bitext.run()


class TMX2BiText():

    def __init__(self):
        self.source_lang = None
        self.target_lang = None
        self.input_path = None            # pathname, file or directory.
        self.outdir = None
        self.filename = None            # filename, the file to be handle.
        self.bitextfp = None
        self.keep_multilines = False

    def setLangs(self, src, tgt):
        self.source_lang = src
        self.target_lang = tgt
        logging.debug("Source lang: {}".format(self.source_lang))
        logging.debug("Target lang: {}".format(self.target_lang))

    def setOutputDir(self, outdir):
        self.outdir = outdir
        logging.debug("Output dir: {}".format(self.outdir))

    def setInputFileDir(self, pathname):
        self.input_path = pathname
        logging.debug("Input dir/file: {}".format(self.input_path))

    def setKeepMultiplelines(self, flag):
        self.keep_multilines = flag

    def run(self):
        """Run the tmx2bitext on file(s)."""
        if os.path.isdir(self.input_path):
            for filename in glob.glob(os.path.join(self.input_path, "*.tmx")):
                self.parse_tmx_file(filename)
        elif os.path.isfile(self.input_path):
            self.parse_tmx_file(self.input_path)

    def output(self, aligns):
        """Write the translation unit in aligns into file."""
        source = aligns[self.source_lang] if self.source_lang in aligns else None
        target = aligns[self.target_lang] if self.target_lang in aligns else None
        tu = self.filterTU(source, target)
        if tu is not None:
            source, target = tu
            line = u'\t'.join([source, target])
            self.bitextfp.write(line + os.linesep)


    def filterTU(self, source, target):
        """filter some obvious non translation units out.

        return None if align is invalid. Or return a pair for tu.

        """
        if source is None or target is None:
            return None

        # handle the multilines seg.
        if len(source.splitlines()) > 1 :
            if self.keep_multilines:
                source = u' '.join(source.splitlines())
            else:
                source = u''

        if len(target.splitlines()) > 1 :
            if self.keep_multilines:
                target = u' '.join(target.splitlines())
            else:
                target = u''

        # convert the sequent spaces into single space.
        source = ' '.join(source.split())
        target = ' '.join(target.split())

        # if no word in source sentence, set the source as empty.
        for word in source.split():
            if word.isalpha():
                break
        else:
            source = ''

        # not a valid TU if source or target is empty.
        if len(source) == 0 or len(target) == 0 :
            return None

        if source == target :
            return None

        return (source, target)

    def parse_tmx_file(self, filename):
        """Parse tmx file, extract the translation units."""

        logging.debug("TMX: {}".format(filename))
        bitext_filename = os.path.basename(filename)
        tmx_filename = bitext_filename
        (bitext_filename, ext) = os.path.splitext(bitext_filename)      # pylint: disable=I0011,W0612
        lang_suffix = '-'.join([LanguageCode(self.source_lang).xx(), LanguageCode(self.target_lang).xx()])
        bitext_filename = '.'.join([bitext_filename, lang_suffix, 'bitext'])
        bitext_filepath = os.path.join(self.outdir, bitext_filename)
        logging.debug("BiText : {}".format(bitext_filepath))

        self.bitextfp = codecs.open(bitext_filepath, 'w', encoding="UTF-8")

        logging.info("TMX : {}".format(tmx_filename))
        logging.info("BiText: {}".format(bitext_filename))

        # Expat parser doesn't support parsing multiple files in parser object.
        # Create parser for each file.
        tmxparser = TMXParser()
        tmxparser.set_output_callback(self.output)
        ret = tmxparser.parse_file(filename)

        result = "Succeed" if ret == 0 else "Failed"
        logging.info("{result}: {filename}".format(result=result, filename=tmx_filename))
        logging.info("")
        self.bitextfp.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
