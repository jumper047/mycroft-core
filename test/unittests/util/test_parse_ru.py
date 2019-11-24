# -*- coding: utf-8 -*-
#
# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import unittest
from datetime import datetime, time

from mycroft.util.parse import extract_datetime
from mycroft.util.parse import extract_number
from mycroft.util.parse import normalize


class TestNormalize(unittest.TestCase):
    def test_articles(self):
        self.assertEqual(
            normalize("dies ist der test", lang="de-de", remove_articles=True),
            "dies ist test")
        self.assertEqual(
            normalize("und noch ein Test", lang="de-de", remove_articles=True),
            "und noch 1 Test")
        self.assertEqual(
            normalize("dies ist der Extra-Test",
                      lang="de-de",
                      remove_articles=False), "dies ist der Extra-Test")

    def test_extract_number(self):
        self.assertEqual(extract_number("dies ist der 1. Test", lang="de-de"),
                         1)

    def test_extractdatetime_de(self):
        def extractWithFormat(text):
            date = datetime(2017, 6, 27, 0, 0)
            [extractedDate, leftover] = extract_datetime(
                text,
                date,
                lang="de-de",
            )
            extractedDate = extractedDate.strftime("%Y-%m-%d %H:%M:%S")
            return [extractedDate, leftover]

        def testExtract(text, expected_date, expected_leftover):
            res = extractWithFormat(text)
            self.assertEqual(res[0], expected_date)
            self.assertEqual(res[1], expected_leftover)

        testExtract(u"setze den frisörtermin auf 5 tage von heute",
                    "2017-07-02 00:00:00", u"setze frisörtermin")

    def test_extractdatetime_default_de(self):
        default = time(9, 0, 0)
        anchor = datetime(2017, 6, 27, 0, 0)
        res = extract_datetime("lass uns treffen am freitag",
                               anchor,
                               lang='de-de',
                               default_time=default)
        self.assertEqual(default, res[0].time())

    def test_spaces(self):
        self.assertEqual(normalize("  dies   ist  ein    test", lang="de-de"),
                         "dies ist 1 test")
        self.assertEqual(
            normalize("  dies   ist  ein    test  ", lang="de-de"),
            "dies ist 1 test")

    def test_numbers(self):
        self.assertEqual(
            normalize("dies ist eins zwei drei test", lang="de-de"),
            "dies ist 1 2 3 test")


if __name__ == "__main__":
    unittest.main()
