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
from collections import OrderedDict
import pymorphy2

_MORPH = pymorphy2.MorphAnalyzer()

_NUM_STRING_RU = {
    0: 'ноль',
    1: 'один',
    2: 'два',
    3: 'три',
    4: 'четыре',
    5: 'пять',
    6: 'шесть',
    7: 'семь',
    8: 'восемь',
    9: 'девять',
    10: 'десять',
    11: 'одиннадцать',
    12: 'двенадцать',
    13: 'тринадцать',
    14: 'четырнадцать',
    15: 'пятнадцать',
    16: 'шестнадцать',
    17: 'семнадцать',
    18: 'восемнадцать',
    19: 'девятнадцать',
    20: 'двадцать',
    30: 'тридцать',
    40: 'сорок',
    50: 'пятьдесят',
    60: 'шестьдесят',
    70: 'семьдесят',
    80: 'восемьдесят',
    90: 'девяносто',
    100: 'сто',
    200: 'двести',
    300: 'триста',
    400: 'четыреста',
    500: 'пятьсот',
    600: 'шестьсот',
    700: 'семьсот',
    800: 'восемьсот',
    900: 'девятьсот'
}


_FRACTION_STRING_RU = {
    2: 'половина',
    3: 'треть',
    4: 'четверть',
    5: 'пятая',
    6: 'шестая',
    7: 'седьмая',
    8: 'восьмая',
    9: 'девятая',
    10: 'десятая',
    11: 'одинадцатая',
    12: 'двенадцатая',
    13: 'тринадцатая',
    14: 'четырнадцатая',
    15: 'пятнадцатая',
    16: 'шестнадцатая',
    17: 'семнадцатая',
    18: 'восемнадцатая',
    19: 'девятнадцатая',
    20: 'двадцатая'
}


_LONG_SCALE_RU = OrderedDict([
    (1000, 'тысяча'),
    (1000000, 'миллион'),
    (1e12, "биллион"),
    (1e18, 'триллион'),
    (1e24, "квадриллион"),
    (1e30, "квинтиллион"),
    (1e36, "секстиллион"),
    (1e42, "септиллион"),
    (1e48, "октиллион"),
    (1e54, "нониллион"),
    (1e60, "дециллион"),
    (1e66, "ундециллион"),
    (1e72, "деодециллион"),
    (1e78, "тредециллион"),
    (1e84, "квадродециллион"),
    (1e90, "квинтодециллион"),
    (1e96, "седециллион"),
    (1e102, "септендециллион"),
    (1e108, "октодециллион"),
    (1e114, "новендесиллион"),
    (1e120, "вигинтиллион"),
    (1e306, "унквинквинквагинциллион"),
    (1e312, "дуоквинквинквагинциллион"),
    (1e336, "сесквинквинквагинциллион"),
    (1e366, "ансексагинтиллион")
])


_SHORT_SCALE_RU = OrderedDict([
    (1000, 'тысяча'),
    (1000000, 'миллион'),
    (1e9, "биллион"),
    (1e12, 'триллион'),
    (1e15, "квадриллион"),
    (1e18, "квинтиллион"),
    (1e21, "секстиллион"),
    (1e24, "септиллион"),
    (1e27, "октиллион"),
    (1e30, "нониллион"),
    (1e33, "дециллион"),
    (1e36, "ундециллион"),
    (1e39, "дуодециллион"),
    (1e42, "тредециллион"),
    (1e45, "кватродециллион"),
    (1e48, "квинквадециллион"),
    (1e51, "седециллион"),
    (1e54, "септендециллион"),
    (1e57, "октодециллион"),
    (1e60, "новендециллион"),
    (1e63, "вигинтиллион"),
    (1e66, "унвигинтиллион"),
    (1e69, "уновигинтиллион"),
    (1e72, "трезвигинтиллион"),
    (1e75, "кваттоурвигинтиллион"),
    (1e78, "квинквавигинтиллион"),
    (1e81, "квесвигинтиллион"),
    (1e84, "септемвигинтиллион"),
    (1e87, "октовигинтиллион"),
    (1e90, "новемвигинтиллион"),
    (1e93, "тригинтиллион"),
    (1e96, "унтригинтиллион"),
    (1e99, "дуотригинтиллион"),
    (1e102, "трестригинтиллион"),
    (1e105, "quattuortrigintillion"),
    (1e108, "quinquatrigintillion"),
    (1e111, "sestrigintillion"),
    (1e114, "septentrigintillion"),
    (1e117, "octotrigintillion"),
    (1e120, "noventrigintillion"),
    (1e123, "quadragintillion"),
    (1e153, "quinquagintillion"),
    (1e183, "sexagintillion"),
    (1e213, "septuagintillion"),
    (1e243, "octogintillion"),
    (1e273, "nonagintillion"),
    (1e303, "centillion"),
    (1e306, "uncentillion"),
    (1e309, "duocentillion"),
    (1e312, "trescentillion"),
    (1e333, "decicentillion"),
    (1e336, "undecicentillion"),
    (1e363, "viginticentillion"),
    (1e366, "unviginticentillion"),
    (1e393, "trigintacentillion"),
    (1e423, "quadragintacentillion"),
    (1e453, "quinquagintacentillion"),
    (1e483, "sexagintacentillion"),
    (1e513, "septuagintacentillion"),
    (1e543, "ctogintacentillion"),
    (1e573, "nonagintacentillion"),
    (1e603, "ducentillion"),
    (1e903, "trecentillion"),
    (1e1203, "quadringentillion"),
    (1e1503, "quingentillion"),
    (1e1803, "sescentillion"),
    (1e2103, "septingentillion"),
    (1e2403, "octingentillion"),
    (1e2703, "nongentillion"),
    (1e3003, "millinillion")
])


_ORDINAL_STRING_BASE_EN = {
    1: 'first',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
    6: 'sixth',
    7: 'seventh',
    8: 'eighth',
    9: 'ninth',
    10: 'tenth',
    11: 'eleventh',
    12: 'twelfth',
    13: 'thirteenth',
    14: 'fourteenth',
    15: 'fifteenth',
    16: 'sixteenth',
    17: 'seventeenth',
    18: 'eighteenth',
    19: 'nineteenth',
    20: 'twentieth',
    30: 'thirtieth',
    40: "fortieth",
    50: "fiftieth",
    60: "sixtieth",
    70: "seventieth",
    80: "eightieth",
    90: "ninetieth",
    10e3: "hundredth",
    1e3: "thousandth"
}


_SHORT_ORDINAL_STRING_EN = {
    1e6: "millionth",
    1e9: "billionth",
    1e12: "trillionth",
    1e15: "quadrillionth",
    1e18: "quintillionth",
    1e21: "sextillionth",
    1e24: "septillionth",
    1e27: "octillionth",
    1e30: "nonillionth",
    1e33: "decillionth"
    # TODO > 1e-33
}
_SHORT_ORDINAL_STRING_EN.update(_ORDINAL_STRING_BASE_EN)


_LONG_ORDINAL_STRING_EN = {
    1e6: "millionth",
    1e12: "billionth",
    1e18: "trillionth",
    1e24: "quadrillionth",
    1e30: "quintillionth",
    1e36: "sextillionth",
    1e42: "septillionth",
    1e48: "octillionth",
    1e54: "nonillionth",
    1e60: "decillionth"
    # TODO > 1e60
}
_LONG_ORDINAL_STRING_EN.update(_ORDINAL_STRING_BASE_EN)
