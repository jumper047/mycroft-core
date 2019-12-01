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
# from datetime import datetime, time

# from mycroft.util.parse import extract_datetime
# from mycroft.util.parse import extract_number
from mycroft.util.parse import normalize


class TestNormalize(unittest.TestCase):
    def test_spaces(self):
        self.assertEqual(normalize("  это   просто  тест", lang="ru-ru"),
                         "это просто тест")
        self.assertEqual(normalize("  это просто    тест   ", lang="ru-ru"),
                         "это просто тест")
        self.assertEqual(normalize("  это просто один тест ", lang="ru-ru"),
                         "это просто 1 тест")

    def test_numbers(self):

        self.assertEqual(normalize("это один два три тест", lang="ru-ru"),
                         "это 1 2 3 тест")
        self.assertEqual(
            normalize("  это четыре пять шесть тест ", lang="ru-ru"),
            "это 4 5 6 тест")
        self.assertEqual(
            normalize("  это семь восемь девять десять тест", lang="ru-ru"),
            "это 7 8 9 10 тест")
        self.assertEqual(
            normalize("это пятьсот одиннадцать двенадцать тест", lang="ru-ru"),
            "это 500 11 12 тест")
        self.assertEqual(
            normalize("тринадцать четырнадцать пятнадцать тест", lang="ru-ru"),
            "13 14 15 тест")
        self.assertEqual(
            normalize("шестнадцать семнадцать восемнадцать тест",
                      lang="ru-ru"), "16 17 18 тест")
        self.assertEqual(
            normalize("а это - девятнадцать двадцать проверка", lang="ru-ru"),
            "а это 19 20 проверка")


if __name__ == "__main__":
    unittest.main()
