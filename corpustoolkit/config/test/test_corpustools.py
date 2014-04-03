#-*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2012, Leo Jiang
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

from corpustoolkit.config.corpustools import CorpusToolsConfig

# To make the test case passed, copy the .corpustools.config into user home.

class TestCorpusToolsConfig():
    def setup(self):
        self.config = CorpusToolsConfig()

    def testOperatorOverride(self):
        # __getitem__, section.option .
        assert(self.config["moses.scripts_path"] == "/moses-suite/moses/scripts")

    def testOperatorOverrideFail01(self):
        # __getitem__, must have the option.
        assert(self.config["moses"] == None)

    def testOperatorOverrideFail02(self):
        # don't support multi-level section.
        assert(self.config["moses.scripts.path"] == None)

    def testOption(self):
        # list the options in section moses.
        assert(self.config.options("moses") == ["path", "scripts_path"])

    def testOptionFail(self):
        # no section named "Moses".
        assert(self.config.options("Moses") == None)
