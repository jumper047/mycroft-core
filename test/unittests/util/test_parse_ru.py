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
from datetime import timedelta  # datetime, time

# from mycroft.util.parse import extract_datetime
from mycroft.util.parse import extract_duration
from mycroft.util.parse import extract_number
from mycroft.util.parse import extract_numbers
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
            "это пятьсот 11 12 тест")
        self.assertEqual(
            normalize("тринадцать четырнадцать пятнадцать тест", lang="ru-ru"),
            "13 14 15 тест")
        self.assertEqual(
            normalize("шестнадцать семнадцать восемнадцать тест",
                      lang="ru-ru"), "16 17 18 тест")
        self.assertEqual(
            normalize("а это - девятнадцать двадцать проверка", lang="ru-ru"),
            "а это 19 20 проверка")

    def test_extract_number(self):
        self.assertEqual(extract_number("это первый тест", lang="ru-ru",
                                        ordinals=True), 1)
        self.assertEqual(extract_number("это 2 тест", lang="ru-ru"), 2)
        self.assertEqual(extract_number("это второй тест", lang="ru-ru",
                                        ordinals=True), 2)
        self.assertEqual(extract_number(
            "это тест номер одна третья", lang="ru-ru"), 1.0 / 3.0)
        self.assertEqual(extract_number(
            "это треть нормального теста", lang="ru-ru"), 1.0 / 3.0)
        self.assertEqual(extract_number("это третий тест",
                                        ordinals=True), 3.0)
        self.assertEqual(extract_number(
            "а это четвёртый кстати говоря", lang="ru-ru", ordinals=True), 4.0)
        self.assertEqual(extract_number("тридцать шестой тест", lang="ru-ru",
                                        ordinals=True), 36.0)
        self.assertEqual(extract_number("это тест номер 4", lang="ru-ru"), 4)
        self.assertEqual(extract_number(
            "одна третья чашки", lang="ru-ru"), 1.0 / 3.0)
        self.assertEqual(extract_number("три чашки", lang="ru-ru"), 3)
        self.assertEqual(extract_number("1/3 чашки", lang="ru-ru"), 1.0 / 3.0)
        self.assertEqual(extract_number("четверть чашки", lang="ru-ru"), 0.25)
        self.assertEqual(extract_number("1/4 чашки", lang="ru-ru"), 0.25)
        self.assertEqual(extract_number(
            "одна четвёртая чашки", lang="ru-ru"), 0.25)
        self.assertEqual(extract_number("2/3 чашки", lang="ru-ru"), 2.0 / 3.0)
        self.assertEqual(extract_number("3/4 чашки", lang="ru-ru"), 3.0 / 4.0)
        self.assertEqual(extract_number("1 и 3/4 чашки", lang="ru-ru"), 1.75)
        self.assertEqual(extract_number(
            "1 чашка с половиной", lang="ru-ru"), 1.5)
        self.assertEqual(extract_number(
            "однч чашка с половиной", lang="ru-ru"), 1.5)
        self.assertEqual(extract_number(
            "одна с половиной чашка", lang="ru-ru"), 1.5)
        self.assertEqual(extract_number(
            "одна целая и одна пятая чашкиs", lang="ru-ru"), 1.5)
        self.assertEqual(extract_number(
            "три четверти чашки", lang="ru-ru"), 3.0 / 4.0)
        self.assertEqual(extract_number(
            "три четвёртых чашки", lang="ru-ru"), 3.0 / 4.0)
        self.assertEqual(extract_number("двадцать два", lang="ru-ru"), 22)
        self.assertEqual(extract_number("девять тысяч", lang="ru-ru"), 9000)
        self.assertEqual(extract_number("две сотни", lang="ru-ru"), 200)
        self.assertEqual(extract_number("двести", lang="ru-ru"), 200)
        self.assertEqual(extract_number(
            "шестьсот шестьдесят шесть", lang="ru-ru"), 666)
        self.assertEqual(extract_number("два миллиона", lang="ru-ru"), 2000000)
        self.assertEqual(extract_number("два миллиона пятьсот тысяч"
                                        "тонн крутящегося металла",
                                        lang="ru-ru"), 2500000)
        self.assertEqual(extract_number(
            "шесть триллионов", lang="ru-ru"), 6000000000000.0)
        self.assertEqual(extract_number("шесть триллионов", lang="ru-ru",
                                        short_scale=False),
                         6e+18)
        self.assertEqual(extract_number("на биллионы лет старше",
                                        lang="ru-ru"),
                         1000000000.0)
        self.assertEqual(extract_number("один точка пять", lang="ru-ru"), 1.5)
        self.assertEqual(extract_number(
            "одна целая пять десятых", lang="ru-ru"), 1.5)
        self.assertEqual(extract_number("один с половиной", lang="ru-ru"), 1.5)
        self.assertEqual(extract_number(
            "три точка четырнадцать", lang="ru-ru"), 3.14)
        self.assertEqual(extract_number("ноль точка два", lang="ru-ru"), 0.2)
        self.assertEqual(extract_number(
            "три целых четырнадцать сотых", lang="ru-ru"), 3.14)
        self.assertEqual(extract_number("две десятых", lang="ru-ru"), 0.2)
        self.assertEqual(extract_number(
            "ноль целых две десятых", lang="ru-ru"), 0.2)
        self.assertEqual(extract_number("на биллионы лет старше", lang="ru-ru",
                                        short_scale=False),
                         1000000000000.0)
        self.assertEqual(extract_number("сотня тысяч", lang="ru-ru"), 100000)
        self.assertEqual(extract_number("минус 2", lang="ru-ru"), -2)
        self.assertEqual(extract_number("минус семьдесят", lang="ru-ru"), -70)
        self.assertEqual(extract_number(
            "тысяча миллионов", lang="ru-ru"), 1000000000)
        self.assertEqual(extract_number("шесть третьих", lang="ru-ru"),
                         6 / 3)
        self.assertEqual(extract_number("шесть третьих", lang="ru-ru",
                                        ordinals=True),
                         6)
        self.assertEqual(extract_number("это биллионный тест", lang="ru-ru",
                                        ordinals=True), 1e09)
        self.assertEqual(extract_number(
            "это биллионный тест", lang="ru-ru"), 1e-9)
        self.assertEqual(extract_number("это биллионный тест", lang="ru-ru",
                                        ordinals=True,
                                        short_scale=False), 1e12)
        self.assertEqual(extract_number("это биллионный тест", lang="ru-ru",
                                        short_scale=False), 1e-12)
        # TODO handle this case
        # self.assertEqual(
        #    extract_number("6 dot six six six"),
        #    6.666)
        self.assertTrue(extract_number(
            "этот игрок в теннис чертовски быстр", lang="ru-ru") is False)
        self.assertTrue(extract_number("парусник", lang="ru-ru") is False)

        self.assertTrue(extract_number("причал 0", lang="ru-ru") is not False)
        self.assertEqual(extract_number("причал ноль", lang="ru-ru"), 0)

        self.assertTrue(extract_number("абыр 0", lang="ru-ru") is not False)
        self.assertEqual(extract_number("абыр 0", lang="ru-ru"), 0)

        self.assertEqual(extract_number("пара кружек пива", lang="ru-ru"), 2)
        self.assertEqual(extract_number(
            "пара сотен кружек пива", lang="ru-ru"), 200)
        self.assertEqual(extract_number(
            "пара тысяч кружек пива", lang="ru-ru"), 2000)

    def test_multiple_numbers(self):
        self.assertEqual(extract_numbers("это один два три тест",
                                         lang="ru-ru"),
                         [1.0, 2.0, 3.0])
        self.assertEqual(extract_numbers("это четыре пять шесть тест",
                                         lang="ru-ru"),
                         [4.0, 5.0, 6.0])
        self.assertEqual(extract_numbers("это десять одиннадцать"
                                         "двенадцать тест", lang="ru-ru"),
                         [10.0, 11.0, 12.0])
        self.assertEqual(extract_numbers("это один двадцать один тест",
                                         lang="ru-ru"),
                         [1.0, 21.0])
        self.assertEqual(extract_numbers("1 собака семь свиней у макдональда",
                                         "была ферма, три раза по 5 макарен",
                                         lang="ru-ru"),
                         [1, 7, 3, 5])
        self.assertEqual(extract_numbers("два раза по два", lang="ru-ru"),
                         [2.0, 2.0])
        self.assertEqual(extract_numbers("двадцать 20 двадцать", lang="ru-ru"),
                         [20, 20, 20])
        self.assertEqual(extract_numbers("двадцать 20 22", lang="ru-ru"),
                         [20.0, 20.0, 22.0])
        self.assertEqual(extract_numbers("двадцать двадцать два двадцать",
                                         lang="ru-ru"),
                         [20, 22, 20])
        self.assertEqual(extract_numbers("двадцать 2", lang="ru-ru"),
                         [22.0])
        self.assertEqual(extract_numbers("двадцать 20 двадцать 2",
                                         lang="ru-ru"),
                         [20, 20, 22])
        self.assertEqual(extract_numbers("шесть триллионов", lang="ru-ru",
                                         short_scale=True),
                         [6e12])
        self.assertEqual(extract_numbers("шесть триллионов", lang="ru-ru",
                                         short_scale=False),
                         [6e18])
        self.assertEqual(extract_numbers("две свиньи и шесть триллионов мух",
                                         lang="ru-ru",
                                         short_scale=True), [2, 6e12])
        self.assertEqual(extract_numbers("две свиньи и шесть триллионов мух",
                                         lang="ru-ru",
                                         short_scale=False), [2, 6e18])
        self.assertEqual(extract_numbers("тридцать две секунды или первый",
                                         lang="ru-ru",
                                         ordinals=True), [32, 1])
        self.assertEqual(extract_numbers("это тест семь восемь девять"
                                         "с половиной", lang="ru-ru"),
                         [7.0, 8.0, 9.5])

    def test_extract_duration_ru(self):
        self.assertEqual(extract_duration("10 секунд", lang="ru-ru"),
                         (timedelta(seconds=10.0), ""))
        self.assertEqual(extract_duration("5 минут", lang="ru=ru"),
                         (timedelta(minutes=5), ""))
        self.assertEqual(extract_duration("2 часа", lang="ru=ru"),
                         (timedelta(hours=2), ""))
        self.assertEqual(extract_duration("3 дня", lang="ru=ru"),
                         (timedelta(days=3), ""))
        self.assertEqual(extract_duration("20 5 недель", lang="ru=ru"),
                         (timedelta(weeks=25), ""))
        self.assertEqual(extract_duration("семь часов", lang="ru=ru"),
                         (timedelta(hours=7), ""))
        self.assertEqual(extract_duration("7.5 секунд", lang="ru=ru"),
                         (timedelta(seconds=7.5), ""))
        self.assertEqual(extract_duration("восемь с половиной дней тридцать"
                                          " девять секунд", lang="ru=ru"),
                         (timedelta(days=8.5, seconds=39), ""))
        self.assertEqual(extract_duration("поставь таймер на тридцать минут",
                                          lang="ru=ru"),
                         (timedelta(minutes=30), "поставь таймер на"))
        self.assertEqual(extract_duration("четыре с половиной минуты до"
                                          " заката", lang="ru=ru"),
                         (timedelta(minutes=4.5), "до заката"))
        self.assertEqual(extract_duration("девятнадцать минут до конца часа",
                                          lang="ru=ru"),
                         (timedelta(minutes=19), "до конца часа"))
        self.assertEqual(extract_duration("разбуди меня через три недели,"
                                          "  четыреста девятнадцать дней"
                                          " и три часа 91.6 секуднд",
                                          lang="ru=ru"),
                         (timedelta(weeks=3, days=497, seconds=391.6),
                             "разбуди меня и"))
        self.assertEqual(extract_duration("фильм идёт один час и пятьдесят"
                                          " семь с половиной минут",
                                          lang="ru=ru"),
                         (timedelta(hours=1, minutes=57.5),
                             "фильм идёт и"))
        self.assertEqual(extract_duration(""), None)


if __name__ == "__main__":
    unittest.main()
