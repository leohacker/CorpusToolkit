#-*- coding: utf-8 -*-

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
