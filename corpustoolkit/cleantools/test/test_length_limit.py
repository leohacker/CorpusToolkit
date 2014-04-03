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

from corpustoolkit.cleantools import length_limit

class TestLengthLimit():
    def setup(self):
        # length of source, target: 24, 25
        self.source_corpus = ur'With the world focused on Iraq, North Korea, and a possible clash with Iran over nuclear weapons, Kosovo has fallen off the radar screen.'
        self.target_corpus = ur'Während sich die Welt auf den Irak, Nordkorea und eine mögliche Auseinandersetzung mit dem Iran über Atomwaffen konzentriert, ist der Kosovo von der Bildfläche verschwunden.'

    def test_length_limit_01(self):
        step = {"name": "length_limit",
                "ext" : "len",
                "source": [1, 24],
                "target": [1, 25]
                }
        result = length_limit.predicate(self.source_corpus, self.target_corpus, step)
        assert result == False

    def test_length_limit_02(self):
        step = {"name": "length_limit",
            "ext" : "len",
            "source": [1, 20],
            "target": [1, 20]
            }
        result = length_limit.predicate(self.source_corpus, self.target_corpus, step)
        assert result == True

    def test_length_limit_03(self):
        step = {"name": "length_limit",
                "ext" : "len",
                "source": [1, 24],
                "target": [1, 24]
                }
        result = length_limit.predicate(self.source_corpus, self.target_corpus, step)
        assert result == True
