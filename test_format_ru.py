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
import datetime

from mycroft.util.lang import get_active_lang, set_active_lang
from mycroft.util.format import nice_number
from mycroft.util.format import nice_time
from mycroft.util.format import pronounce_number
from mycroft.util.lang.format_ru import nice_response_ru
from mycroft.util.lang.format_ru import pronounce_ordinal_ru
from mycroft.util.format import join_list


# fractions are not capitalized for now
NUMBERS_FIXTURE_RU = {
    1.435634: '1,436',
    2: '2',
    5.0: '5',
    1234567890: '1234567890',
    12345.67890: '12345,679',
    0.027: '0,027',
    0.5: 'половина',
    1.333: '1 целая и 1 треть',
    2.666: '2 целых 2 трети',
    0.25: 'четверть',
    1.25: '1 целая и 1 четверть',
    0.75: '3 четверти',
    1.75: '1 целая и 3 четверти', 
    3.4: '3 целых и 2 пятых',
    16.8333: '16 целых и 5 шестых',
    12.5714: '12 целых 4 седьмых',
    9.625: '9 целых и 5 восьмых',
    6.777: '6 целых и 7 девятых',
    3.1: '3 целых и 1 десятая',
    2.272: '2 целых и 3 одинадцатых',
    5.583: '5 целых и 7 двенадцатых',
    8.384: '8 целых и 5 тринадцатых',
    0.071: '1 четырнадцатая',
    6.466: '6 целых и 7 пятнадцатых',
    8.312: '8 целых и 5 шестнадцатых',
    2.176: '2 целых и 3 семнадцатых',
    200.722: '200 целых и  13 восемнадцатых',
    7.421: '7 целых 8 девятнадцатых',
    0.05: '1 двадцатая'
}


class TestNiceNumberFormat(unittest.TestCase):
    def setUp(self):
        self.old_lang = get_active_lang()
        set_active_lang("ru-ru")

    def tearDown(self):
        set_active_lang(self.old_lang)

    def test_convert_float_to_nice_number(self):
        for number, number_str in NUMBERS_FIXTURE_RU.items():
            self.assertEqual(nice_number(number), number_str,
                             'should format {} as {} and not {}'.format(
                                 number, number_str,
                                 nice_number(number)))

    def test_specify_denominator(self):
        self.assertEqual(nice_number(5.5, denominators=[1, 2, 3]),
                         '5 с половиной',
                         'should format 5.5 as \
                         5 с половиной and not {}'.format(
                             nice_number(5.5, denominators=[1, 2, 3])))
        self.assertEqual(nice_number(2.333, denominators=[1, 2]),
                         '2,333',
                         'should format 2,333 as 2,333 not {}'.format(
                             nice_number(2.333,
                                         denominators=[1, 2])))

    def test_no_speech(self):
        self.assertEqual(nice_number(6.777, speech=False),
                         '6 7/9',
                         'should format 6.777 as 6 7/9 not {}'.format(
                             nice_number(6.777, speech=False)))
        self.assertEqual(nice_number(6.0, speech=False),
                         '6',
                         'should format 6.0 as 6 not {}'.format(
                             nice_number(6.0, speech=False)))


class TestPronounceNumber(unittest.TestCase):
    def setUp(self):
        self.old_lang = get_active_lang()
        set_active_lang("ru-ru")

    def tearDown(self):
        set_active_lang(self.old_lang)

    def test_convert_int_ru(self):
        self.assertEqual(pronounce_number(1), "один")
        self.assertEqual(pronounce_number(10), "десять")
        self.assertEqual(pronounce_number(15), "пятнадцать")
        self.assertEqual(pronounce_number(20), "двадцать")
        self.assertEqual(pronounce_number(27), "двадцать семь")
        self.assertEqual(pronounce_number(30), "тридцать")
        self.assertEqual(pronounce_number(33), "тридцать три")

        self.assertEqual(pronounce_number(71), "семьдесят один")
        self.assertEqual(pronounce_number(80), "восемьдесят")
        self.assertEqual(pronounce_number(74), "семьдесят четыре")
        self.assertEqual(pronounce_number(79), "семьдесят девять")
        self.assertEqual(pronounce_number(91), "девяносто один")
        self.assertEqual(pronounce_number(97), "девяносто семь")
        self.assertEqual(pronounce_number(300), "триста")

    def test_convert_negative_int_ru(self):
        self.assertEqual(pronounce_number(-1), "минус один")
        self.assertEqual(pronounce_number(-10), "минус десять")
        self.assertEqual(pronounce_number(-15), "минус пятнадцать")
        self.assertEqual(pronounce_number(-20), "минус двадцать")
        self.assertEqual(pronounce_number(-27), "минус двадцать семь")
        self.assertEqual(pronounce_number(-30), "минус тридцать")
        self.assertEqual(pronounce_number(-33), "минус тридцать три")

    def test_convert_decimals_ru(self):
        self.assertEqual(pronounce_number(1.234),
                         "одна целая двадцать три сотых")
        self.assertEqual(pronounce_number(21.234),
                         "двадцать одна целая двадцать три сотых")
        self.assertEqual(pronounce_number(21.234, places=1),
                         "двадцать одна целая две десятых")
        self.assertEqual(pronounce_number(21.234, places=0),
                         "двадцать один")
        self.assertEqual(pronounce_number(21.234, places=3),
                         "двадцать одна целая двести тридцать четыре тысячных")
        self.assertEqual(pronounce_number(21.234, places=4),
                         "двадцать одна целая двести тридцать четыре тысячных")
        self.assertEqual(pronounce_number(21.234, places=5),
                         "двадцать одна целая двести тридцать четыре тысячных")
        self.assertEqual(pronounce_number(-1.234),
                         "минус одна целая двадцать три сотых")
        self.assertEqual(pronounce_number(-21.234),
                         "минус двадцать одна целая двадцать три сотых")
        self.assertEqual(pronounce_number(-21.234, places=1),
                         "минус двадцать одна целая две сотых")
        self.assertEqual(pronounce_number(-21.234, places=0),
                         "минус двадцать один")
        self.assertEqual(pronounce_number(-21.234, places=3),
                         "минус двадцать одна целая двести тридцать четыре тысячных")
        self.assertEqual(pronounce_number(-21.234, places=4),
                         "минус двадцать одна целая двести тридцать четыре тысячных")
        self.assertEqual(pronounce_number(-21.234, places=5),
                         "минус двадцать одна целая двести тридцать четыре тысячных")

    def test_convert_scientific_notation(self):
        self.assertEqual(pronounce_number(0, scientific=True), "ноль")
        self.assertEqual(pronounce_number(33, scientific=True),
                         "три целых и три десятых на десять в степени один")
        self.assertEqual(pronounce_number(299792458, scientific=True),
                         "две целых девяносто девять сотых на десять в степени восемь")
        self.assertEqual(pronounce_number(299792458, places=6,
                                          scientific=True),
                         "две целых девятьсот девяносто семь тысяч девятьсот двадцать пять "
                         "на десять в степени восемь")
        self.assertEqual(pronounce_number(1.672e-27, places=3,
                                          scientific=True),
                         "one point six seven two times ten to the power of "
                         "negative twenty seven")

    def test_large_numbers(self):
        self.assertEqual(
            pronounce_number(299792458, short_scale=True),
            "two hundred and ninety nine million, seven hundred "
            "and ninety two thousand, four hundred and fifty eight")
        self.assertEqual(
            pronounce_number(299792458, short_scale=False),
            "two hundred and ninety nine million, seven hundred "
            "and ninety two thousand, four hundred and fifty eight")
        self.assertEqual(
            pronounce_number(100034000000299792458, short_scale=True),
            "one hundred quintillion, thirty four quadrillion, "
            "two hundred and ninety nine million, seven hundred "
            "and ninety two thousand, four hundred and fifty eight")
        self.assertEqual(
            pronounce_number(100034000000299792458, short_scale=False),
            "one hundred trillion, thirty four thousand billion, "
            "two hundred and ninety nine million, seven hundred "
            "and ninety two thousand, four hundred and fifty eight")
        self.assertEqual(
            pronounce_number(10000000000, short_scale=True),
            "ten billion")
        self.assertEqual(
            pronounce_number(1000000000000, short_scale=True),
            "one trillion")
        # TODO maybe beautify this
        self.assertEqual(
            pronounce_number(1000001, short_scale=True),
            "one million, one")


class TestNiceDateFormat_de(unittest.TestCase):
    def setUp(self):
        self.old_lang = get_active_lang()
        set_active_lang("de-de")

    def tearDown(self):
        set_active_lang(self.old_lang)

    def test_convert_times_de(self):
        dt = datetime.datetime(2017, 1, 31,
                               13, 22, 3)

        self.assertEqual(nice_time(dt),
                         "ein Uhr zweiundzwanzig")
        self.assertEqual(nice_time(dt, use_ampm=True),
                         "ein Uhr zweiundzwanzig nachmittags")
        self.assertEqual(nice_time(dt, speech=False),
                         "1:22")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_ampm=True),
                         "1:22 PM")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True),
                         "13:22")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:22")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=True),
                         "dreizehn Uhr zweiundzwanzig")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=False),
                         "dreizehn Uhr zweiundzwanzig")

        dt = datetime.datetime(2017, 1, 31,
                               13, 0, 3)
        self.assertEqual(nice_time(dt),
                         "ein Uhr")
        self.assertEqual(nice_time(dt, use_ampm=True),
                         "ein Uhr nachmittags")
        self.assertEqual(nice_time(dt, speech=False),
                         "1:00")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_ampm=True),
                         "1:00 PM")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True),
                         "13:00")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:00")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=True),
                         "dreizehn Uhr")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=False),
                         "dreizehn Uhr")

        dt = datetime.datetime(2017, 1, 31,
                               13, 2, 3)
        self.assertEqual(nice_time(dt),
                         "ein Uhr zwei")
        self.assertEqual(nice_time(dt, use_ampm=True),
                         "ein Uhr zwei nachmittags")
        self.assertEqual(nice_time(dt, speech=False),
                         "1:02")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_ampm=True),
                         "1:02 PM")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True),
                         "13:02")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:02")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=True),
                         "dreizehn Uhr zwei")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=False),
                         "dreizehn Uhr zwei")

        dt = datetime.datetime(2017, 1, 31,
                               0, 2, 3)
        self.assertEqual(nice_time(dt),
                         u"zwölf Uhr zwei")
        self.assertEqual(nice_time(dt, use_ampm=True),
                         u"zwölf Uhr zwei nachts")
        self.assertEqual(nice_time(dt, speech=False),
                         "12:02")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_ampm=True),
                         "12:02 AM")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True),
                         "00:02")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True, use_ampm=True),
                         "00:02")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=True),
                         "null Uhr zwei")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=False),
                         "null Uhr zwei")

        dt = datetime.datetime(2017, 1, 31,
                               12, 15, 9)
        self.assertEqual(nice_time(dt),
                         u"zwölf Uhr fünfzehn")
        self.assertEqual(nice_time(dt, use_ampm=True),
                         u"zwölf Uhr fünfzehn nachmittags")
        self.assertEqual(nice_time(dt, speech=False),
                         "12:15")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_ampm=True),
                         "12:15 PM")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True),
                         "12:15")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True, use_ampm=True),
                         "12:15")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=True),
                         u"zwölf Uhr fünfzehn")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=False),
                         u"zwölf Uhr fünfzehn")

        dt = datetime.datetime(2017, 1, 31,
                               19, 40, 49)
        self.assertEqual(nice_time(dt),
                         "sieben Uhr vierzig")
        self.assertEqual(nice_time(dt, use_ampm=True),
                         "sieben Uhr vierzig abends")
        self.assertEqual(nice_time(dt, speech=False),
                         "7:40")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_ampm=True),
                         "7:40 PM")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True),
                         "19:40")
        self.assertEqual(nice_time(dt, speech=False,
                                   use_24hour=True, use_ampm=True),
                         "19:40")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=True),
                         "neunzehn Uhr vierzig")
        self.assertEqual(nice_time(dt, use_24hour=True,
                                   use_ampm=False),
                         "neunzehn Uhr vierzig")

        dt = datetime.datetime(2017, 1, 31,
                               1, 15, 00)
        self.assertEqual(nice_time(dt, use_24hour=True),
                         u"ein Uhr fünfzehn")

        dt = datetime.datetime(2017, 1, 31,
                               1, 35, 00)
        self.assertEqual(nice_time(dt),
                         u"ein Uhr fünfunddreißig")

        dt = datetime.datetime(2017, 1, 31,
                               1, 45, 00)
        self.assertEqual(nice_time(dt),
                         u"ein Uhr fünfundvierzig")

        dt = datetime.datetime(2017, 1, 31,
                               4, 50, 00)
        self.assertEqual(nice_time(dt),
                         u"vier Uhr fünfzig")

        dt = datetime.datetime(2017, 1, 31,
                               5, 55, 00)
        self.assertEqual(nice_time(dt),
                         u"fünf Uhr fünfundfünfzig")

        dt = datetime.datetime(2017, 1, 31,
                               5, 30, 00)
        self.assertEqual(nice_time(dt, use_ampm=True),
                         u"fünf Uhr dreißig morgens")


class TestJoinList_de(unittest.TestCase):
    def setUp(self):
        self.old_lang = get_active_lang()
        set_active_lang("de-de")

    def tearDown(self):
        set_active_lang(self.old_lang)

    def test_join_list_de(self):
        self.assertEqual(join_list(['Hallo', 'Auf wieder Sehen'], 'and'),
                         'Hallo und Auf wieder Sehen')

        self.assertEqual(join_list(['A', 'B', 'C'], 'or'),
                         'A, B oder C')


if __name__ == "__main__":
    unittest.main()
