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
from datetime import timedelta, datetime

from mycroft.util.parse import extract_datetime
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
                                         " двенадцать тест", lang="ru-ru"),
                         [10.0, 11.0, 12.0])
        self.assertEqual(extract_numbers("это один двадцать один тест",
                                         lang="ru-ru"),
                         [1.0, 21.0])
        self.assertEqual(extract_numbers("1 собака семь свиней у макдональда"
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
        self.assertEqual(extract_numbers("две свиньи и шесть триллионов мух",
                                         lang="ru-ru",
                                         short_scale=True), [2, 6e12])
        self.assertEqual(extract_numbers("тридцать две секунды или первый",
                                         lang="ru-ru",
                                         ordinals=True), [32, 1])
        self.assertEqual(extract_numbers("это тест семь восемь девять"
                                         " с половиной", lang="ru-ru"),
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
                                          " четыреста девятнадцать дней"
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

    def test_extractdatetime_ru(self):
        def extractWithFormat(text):
            date = datetime(2017, 6, 27, 13, 4)  # Tue June 27, 2017 @ 1:04pm
            [extractedDate, leftover] = extract_datetime(text, date)
            extractedDate = extractedDate.strftime("%Y-%m-%d %H:%M:%S")
            return [extractedDate, leftover]

        def testExtract(text, expected_date, expected_leftover):
            res = extractWithFormat(normalize(text))
            self.assertEqual(res[0], expected_date, "for=" + text)
            self.assertEqual(res[1], expected_leftover, "for=" + text)

        testExtract("сейчас самое время",
                    "2017-06-27 13:04:00", "самое время")
        testExtract("через секунду",
                    "2017-06-27 13:04:01", "")
        testExtract("через пару секунд",
                    "2017-06-27 13:04:02", "")
        testExtract("через минуту",
                    "2017-06-27 13:05:00", "")
        testExtract("через пару минут",
                    "2017-06-27 13:06:00", "")
        testExtract("через пару часов",
                    "2017-06-27 15:04:00", "")
        testExtract("через пару недель",
                    "2017-07-11 00:00:00", "")
        testExtract("через пару месяцев",
                    "2017-08-27 00:00:00", "")
        testExtract("через пару лет",
                    "2019-06-27 00:00:00", "")
        testExtract("через десятилетие",
                    "2027-06-27 00:00:00", "")
        testExtract("через пару десятилетий",
                    "2037-06-27 00:00:00", "")
        testExtract("следующее десятилетие",
                    "2027-06-27 00:00:00", "")
        testExtract("через столетие",
                    "2117-06-27 00:00:00", "")
        testExtract("через тысячелетие",
                    "3017-06-27 00:00:00", "")
        testExtract("через пару десятилетий",
                    "2037-06-27 00:00:00", "")
        testExtract("через 5 десятилетий",
                    "2067-06-27 00:00:00", "")
        testExtract("через пару столетий",
                    "2217-06-27 00:00:00", "")
        testExtract("через 2 столетий",
                    "2217-06-27 00:00:00", "")
        testExtract("через пару тысячелетий",
                    "4017-06-27 00:00:00", "")
        testExtract("через пару of тысячелетий",
                    "4017-06-27 00:00:00", "")
        testExtract("через час",
                    "2017-06-27 14:04:00", "")
        testExtract("мне это нужно через час",
                    "2017-06-27 14:04:00", "мне это нужно")
        testExtract("через 1 секунду",
                    "2017-06-27 13:04:01", "")
        testExtract("через 2 секунды",
                    "2017-06-27 13:04:02", "")
        testExtract("поставь засаду через 1 минуту",
                    "2017-06-27 13:05:00", "поставь засаду")
        testExtract("поставь засаду через пол часа",
                    "2017-06-27 13:34:00", "поставь засаду")
        testExtract("поставь засаду через пять дней",
                    "2017-07-02 00:00:00", "поставь засаду")
        testExtract("поставь засаду через пять дней после вторника",
                    "2017-07-02 00:00:00", "поставь засаду")
        testExtract("поставь засаду через два дня после следующей пятницы в пять ноль ноль",
                    "2017-07-09 05:00:00", "поставь засаду")
        testExtract("опиши засаду через два дня после следующей пятницы в пять ноль ноль",
                    "2017-06-25 05:00:00", "опиши засаду")
        testExtract("что за день после завтра погода",
                    "2017-06-29 00:00:00", "что за погода")
        testExtract("день после завтра",
                    "2017-06-29 00:00:00", "")
        testExtract("напомни мне в 10:45",
                    "2017-06-27 22:45:00", "напомни мне")
        testExtract("какая погода будет в пятницу утром",
                    "2017-06-30 08:00:00", "какая погода будет")
        testExtract("какая погода будет сегодня",
                    "2017-06-28 00:00:00", "какая погода будет")
        testExtract("какая погода будет после обеда",
                    "2017-06-27 15:00:00", "какая погода будет")
        testExtract("какая погода будет этим вечером",
                    "2017-06-27 19:00:00", "какая погода будет")
        testExtract("какая погода была этим утром?",
                    "2017-06-27 08:00:00", "какая погода была")
        testExtract("напомни мне позвонить маме через 8 недель и 2 дня",
                    "2017-08-24 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме 3го августа",
                    "2017-08-03 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне завтра позвонить маме в 7 утра",
                    "2017-06-28 07:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне завтра позвонить маме в 10 вечера",
                    "2017-06-28 22:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 7 утра",
                    "2017-06-28 07:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через час",
                    "2017-06-27 14:04:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 17:30",
                    "2017-06-27 17:30:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 6:30",
                    "2017-06-28 06:30:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 6 30",
                    "2017-06-28 06:30:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 6 30",
                    "2017-06-28 06:30:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 6 30",
                    "2017-06-28 06:30:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме ровно в 7",
                    "2017-06-27 19:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме этим вечером ровно в 7",
                    "2017-06-27 19:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме ровно в семь вечера",
                    "2017-06-27 19:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме ровно в семь утра",
                    "2017-06-28 07:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 7:00 утра",
                    "2017-06-28 07:00:00", "напомни мне позвонить маме")
        testExtract("7 утра",
                    "2017-06-28 07:00:00", "")
        testExtract("напомни мне позвонить маме в четверг вечером ровно в семь",
                    "2017-06-29 19:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в четверг утром ровно в семь",
                    "2017-06-29 07:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в ровно в семь четверг утром",
                    "2017-06-29 07:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 7:00 четверг утром",
                    "2017-06-29 07:00:00", "напомни мне позвонить маме")
        # TODO: This test is imperfect due to the "в 7:00" still in the
        #       remainder.  But let it pass for now since time is correct
        testExtract("напомни мне позвонить маме в 7:00 четверг вечером",
                    "2017-06-29 19:00:00", "напомни мне позвонить маме в 7:00")
        testExtract("напомни мне позвонить маме в 8 вечером среды",
                    "2017-06-28 20:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 8 среду вечером",
                    "2017-06-28 20:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в среду вечером в 8",
                    "2017-06-28 20:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через два часа",
                    "2017-06-27 15:04:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 2 часа",
                    "2017-06-27 15:04:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через 15 минут",
                    "2017-06-27 13:19:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через пятнадцать минут",
                    "2017-06-27 13:19:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через пол часа",
                    "2017-06-27 13:34:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через четверть часа",
                    "2017-06-27 13:34:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через четверть часа",
                    "2017-06-27 13:19:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через четверть часа",
                    "2017-06-27 13:19:00", "напомни мне позвонить маме")
        testExtract("играй музыку рика эштли 2 дня после пятницы",
                    "2017-07-02 00:00:00", "играй музыку рика эштли")
        testExtract("начни вторжение в 3:45 pm в четверг",
                    "2017-06-29 15:45:00", "начни вторжение")
        testExtract("в понедельник закажи пирог в пекарне",
                    "2017-07-03 00:00:00", "закажи пирог в пекарне")
        testExtract("играй днерожденческую музыку пять лет начиная с сегодня",
                    "2022-06-27 00:00:00", "играй днерожденческую музыку")
        testExtract("позвонить маме в 12:45 в следующий четверг",
                    "2017-07-06 12:45:00", "позвонить маме")
        testExtract("какая погодa будет в следующую среду",
                    "2017-07-05 00:00:00", "какая погода будет")
        testExtract("какая погода будет в следюущий четверг?",
                    "2017-07-06 00:00:00", "какая погода будет")
        testExtract("какая погода будет в следующую пятницу?",
                    "2017-06-30 00:00:00", "какая погода будет")
        testExtract("какая погода будет в следующую пятницу утром",
                    "2017-06-30 08:00:00", "какая погода будет")
        testExtract("какая погода будет в следующую пятницу вечером",
                    "2017-06-30 19:00:00", "какая погода будет")
        testExtract("какая погода будет в следующую пятницу после обеда",
                    "2017-06-30 15:00:00", "какая погода будет")
        testExtract("напомни мне позвонить маме третьего августа",
                    "2017-08-03 00:00:00", "напомни мне позвонить маме")
        testExtract("купить фейрверки 4го июля",
                    "2017-07-04 00:00:00", "купить фейрверки")
        testExtract("какая погода будет через две недели после следующей пятницы",
                    "2017-07-14 00:00:00", "какая погода")
        testExtract("какая погода будет в среду в 7:00",
                    "2017-06-28 07:00:00", "какая погода")
        testExtract("поставь будильник на среду ровно в семь",
                    "2017-06-28 07:00:00", "поставь будильник")
        testExtract("поставь напоминание на 12:45 дня в следующий четверг",
                    "2017-07-06 12:45:00", "поставь напоминание")
        testExtract("какая погода будет в этот четверг?",
                    "2017-06-29 00:00:00", "какая погода")
        testExtract("запланируй посещение через две недели и 6 дней после субботы",
                    "2017-07-21 00:00:00", "запланируй посещение")
        testExtract("начни вторжение в три сорок пять в четверг",
                    "2017-06-29 03:45:00", "начни вторжение")
        testExtract("начни вторжение в 8 часов в четверг",
                    "2017-06-29 08:00:00", "начни вторжение")
        testExtract("начни вечеринку ровно в 8 вечера в четверг",
                    "2017-06-29 20:00:00", "начни вечеринку")
        testExtract("начни вторжение в 8 вечера в четверг",
                    "2017-06-29 20:00:00", "начни вторжение")
        testExtract("начни вторжение в полдень четверга",
                    "2017-06-29 12:00:00", "начни вторжение")
        testExtract("начни вторжение on четверг в полночь",
                    "2017-06-29 00:00:00", "начни вторжение")
        testExtract("начни вторжение on четверг в 5:00",
                    "2017-06-29 05:00:00", "начни вторжение")
        testExtract("начни вторжение в 0500 через один день после понедельника",
                    "2017-07-04 05:00:00", "начни вторжение")
        testExtract("напомни мне проснуться через 4 года",
                    "2021-06-27 00:00:00", "напомни мне проснуться")
        testExtract("напомни мне проснуться через 4 года и четыре дня",
                    "2021-07-01 00:00:00", "напомни мне проснуться")
        testExtract("какая погода будет через 3 дня после завтра",
                    "2017-07-01 00:00:00", "какая погода")
        testExtract("3 декабря"
                    "2017-12-03 00:00:00", "")
        testExtract("давай встретимся в 8:00 вечера",
                    "2017-06-27 20:00:00", "давай встретимся")
        testExtract("давай встретимся в 5 вечера",
                    "2017-06-27 17:00:00", "давай встретимся")
        testExtract("давай встретимся в 8 a.m.",
                    "2017-06-28 08:00:00", "давай встретимся")
        testExtract("напомни мне проснуться в 8 утра",
                    "2017-06-28 08:00:00", "напомни мне проснуться")
        testExtract("какя погода будет в четверг?",
                    "2017-06-27 00:00:00", "какая погода")
        testExtract("какая погода будет в понедельник",
                    "2017-07-03 00:00:00", "какая погода")
        testExtract("какая погода будет в эту среду",
                    "2017-06-28 00:00:00", "какая погода")
        testExtract("в четверг какая будет погода",
                    "2017-06-29 00:00:00", "какая будет погода")
        testExtract("в этот четверг какая будет погода",
                    "2017-06-29 00:00:00", "какая погода")
        testExtract("какая погода была в прошлый понедельник",
                    "2017-06-26 00:00:00", "какая была погода")
        testExtract("поставь будильник на вечер среды в 8",
                    "2017-06-28 20:00:00", "поставь будильник")
        testExtract("поставь будильник на среду ровно на 3 часа дня",
                    "2017-06-28 15:00:00", "поставь будильник")
        testExtract("поставь будильник на среду в 3:00 дня",
                    "2017-06-28 15:00:00", "поставь будильник")
        testExtract("поставь будильник на среду ровно в 3 утра",
                    "2017-06-28 03:00:00", "поставь будильник")
        testExtract("поставь будильник на среду утром в ровно в семь",
                    "2017-06-28 07:00:00", "поставь будильник")
        testExtract("поставь будильник в ровно в семь на сегодня",
                    "2017-06-27 19:00:00", "поставь будильник")
        testExtract("поставь будильник на этот вечер в ровно в семь",
                    "2017-06-27 19:00:00", "поставь будильник")
        testExtract("поставь будильник на 7:00 вечера",
                    "2017-06-27 19:00:00", "поставь будильник")
        testExtract("поставь будильник на 7:00 на этот вечер",
                    "2017-06-27 19:00:00", "поставь будильник")
        # TODO: This test is imperfect due to the "в 7:00" still in the
        #       remainder.  But let it pass for now since time is correct
        testExtract("поставь будильник на этот вечер в 7:00",
                    "2017-06-27 19:00:00", "поставь будильник в 7:00")
        testExtract("поставь будильник на 7:00 этим вечером",
                    "2017-06-27 19:00:00", "поставь будильник")
        testExtract("поставь будильник на 7:00 этим утром",
                    "2017-06-27 07:00:00", "поставь будильник")
        testExtract("поставь будильник на 7:00 в ночь",
                    "2017-06-27 19:00:00", "поставь будильник")
        testExtract("поставь будильник на 4:00 в ночи",
                    "2017-06-27 16:00:00", "поставь будильник")
        testExtract("вечером 5го июня 2017 напомни мне" +
                    " позвонить маме",
                    "2017-06-05 19:00:00", "напомни мне позвонить маме")
        testExtract("вечером 5го августа 2017 напомни мне" +
                    " позвонить маме",
                    "2017-08-05 19:00:00", "напомни мне позвонить маме")
        testExtract("вечером 5го августа 2017 напомни мне" +
                    " позвонить маме",
                    "2017-08-05 19:00:00", "напомни мне позвонить маме")
        # TODO: This test is imperfect due to the missing "for" in the
        #       remainder.  But let it pass for now since time is correct
        testExtract("добавь в мой календарь встречу с джулиусом утром" +
                    " четвёртого марта",
                    "2018-03-04 08:00:00",
                    "добавь в мой календарь встречу с джулиусом")
        testExtract("напомни мне позвонить маме в следующий вторник",
                    "2017-07-04 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через 3 недели",
                    "2017-07-18 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через 8 недель",
                    "2017-08-22 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через 8 недель и два дня",
                    "2017-08-24 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через 4 дня",
                    "2017-07-01 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через 3 месяца",
                    "2017-09-27 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме через 2 года и 2 дня",
                    "2019-06-29 00:00:00", "напомни мне позвонить маме")
        testExtract("я должен был позвонить маме на прошлой неделе",
                    "2017-06-20 00:00:00", "я должен был позвонить маме")
        testExtract("напомни мне позвонить маме на следующей неделе",
                    "2017-07-04 00:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 10am в субботу",
                    "2017-07-01 10:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 10am в эту субботу",
                    "2017-07-01 10:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 10 в следующую субботу",
                    "2017-07-01 10:00:00", "напомни мне позвонить маме")
        testExtract("напомни мне позвонить маме в 10am в следующую субботу",
                    "2017-07-01 10:00:00", "напомни мне позвонить маме")
        testExtract("я должен был позвонить маме в прошлом месяце",
                    "2017-06-20 00:00:00", "я должен был позвонить маме")
        testExtract("напомни мне позвонить маме в следующем месяце",
                    "2017-07-27 00:00:00", "напомни мне позвонить маме")
        testExtract("я должен был позвонить маме в прошлом месяце",
                    "2017-06-20 00:00:00", "я должен был позвонить маме")
        testExtract("я должен был позвонить маме в прошлом году",
                    "2016-06-27 00:00:00", "я должен был позвонить мамe")
        testExtract("напомни мне позвонить маме в следующем году",
                    "2018-06-27 00:00:00", "напомни мне позвонить маме")
        # Below two tests, ensure thв time is picked
        # even if no am/pm is specified
        # in case of weekdays/tonight
        testExtract("поставь будильник на 9 по будням",
                    "2017-06-27 21:00:00", "поставь будильник по будням")
        testExtract("в 8 вечера",
                    "2017-06-27 20:00:00", "")
        testExtract("в 8:30 ночи",
                    "2017-06-27 20:30:00", "")
        # Tests a time with ':' & without am/pm
        testExtract("поставь будильник на 9:30 вечера",
                    "2017-06-27 21:30:00", "поставь будильник")
        testExtract("поставь будильник на 9:00 вечера",
                    "2017-06-27 21:00:00", "поставь будильник")
        # Check if it picks the intent irrespective of correctness
        testExtract("поставь будильник ровно на 9 вечера",
                    "2017-06-27 21:00:00", "поставь будильник")
        testExtract("напомни мне про игру сегодня вечером в 11:30",
                    "2017-06-27 23:30:00", "напомни мне про игру")
        testExtract("поставь будильник в 7:30 по будням",
                    "2017-06-27 19:30:00", "поставь будильник по будням")

    def test_extract_ambiguous_time_ru(self):
        morning = datetime(2017, 6, 27, 8, 1, 2)
        evening = datetime(2017, 6, 27, 20, 1, 2)
        noonish = datetime(2017, 6, 27, 12, 1, 2)
        self.assertEqual(
            extract_datetime('покорми рыбу ровно в десять', morning)[0],
            datetime(2017, 6, 27, 10, 0, 0))
        self.assertEqual(
            extract_datetime('покорми рыбу ровно в десять', noonish)[0],
            datetime(2017, 6, 27, 22, 0, 0))
        self.assertEqual(
            extract_datetime('покорми рыбу ровно в десять', evening)[0],
            datetime(2017, 6, 27, 22, 0, 0))

    def test_extract_relativedatetime_ru(self):
        def extractWithFormв(text):
            date = datetime(2017, 6, 27, 10, 1, 2)
            [extractedDвe, leftover] = extract_datetime(text, date)
            extractedDвe = extractedDвe.strftime("%Y-%m-%d %H:%M:%S")
            return [extractedDвe, leftover]

        def testExtract(text, expected_date, expected_leftover):
            res = extractWithFormв(normalize(text))
            self.assertEqual(res[0], expected_date, "for=" + text)
            self.assertEqual(res[1], expected_leftover, "for=" + text)

        testExtract("давай встретимся через 5 минут",
                    "2017-06-27 10:06:02", "давай встретимся")
        testExtract("давай встретимся через 5 минут",
                    "2017-06-27 10:06:02", "давай встретимся")
        testExtract("давай встретимся через 5 секунд",
                    "2017-06-27 10:01:07", "давай встретимся")
        testExtract("давай встретимся через 1 час",
                    "2017-06-27 11:01:02", "давай встретимся")
        testExtract("давай встретимся через 2 часа",
                    "2017-06-27 12:01:02", "давай встретимся")
        testExtract("давай встретимся через 2 часа",
                    "2017-06-27 12:01:02", "давай встретимся")
        testExtract("давай встретимся через 1 минуту",
                    "2017-06-27 10:02:02", "давай встретимся")
        testExtract("давай встретимся через 1 секунду",
                    "2017-06-27 10:01:03", "давай встретимся")
        testExtract("давай встретимся через 5 секунд",
                    "2017-06-27 10:01:07", "давай встретимся")


if __name__ == "__main__":
    unittest.main()
