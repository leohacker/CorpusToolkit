# -*- coding: utf-8 -*-

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

from nose.tools import assert_raises
from nose.tools import raises
from corpustoolkit.language_code import LanguageCode


class TestLanguageCode:
    def check_constructor(self, param, value):
        lc = LanguageCode(param)
        assert lc._langcode == value

    def test_constructor(self):
        params = ["eng", "Chinses", "AB_AE",
                  "en_US", "zh_cn", "zh",    "EN-US",
                  "zh-CN.gbk", "en_US.UTF-8"]
        result = [None, None, None,
                  "en_US", "zh_CN", "zh_CN", "en_US",
                  "zh_CN", "en_US"]
        for param, value in zip(params, result):
            yield self.check_constructor, param, value

    def test_xx(self):
        lc = LanguageCode("en-US")
        assert lc.xx() == "en"

    def test_xx_XX(self):
        lc = LanguageCode("zh_tw")
        assert lc.xx_XX() == "zh_TW"

    def test_TMX_form(self):
        lc = LanguageCode("zh_CN")
        assert lc.TMX_form() == "zh-CN"
