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

from mycroft.util.lang.format_common import convert_to_mixed_fraction
from mycroft.util.log import LOG
from mycroft.util.lang.common_data_ru import (_NUM_STRING_RU,
                                              _FRACTION_STRING_RU,
                                              _SPECIAL_FRACTION_STRING_RU,
                                              _SHORT_SCALE_FRACTION_STRING_RU,
                                              _LONG_SCALE_FRACTION_STRING_RU,
                                              _SPECIAL_TIME_RU,
                                              _SPECIAL_MIN_RU,
                                              _LONG_SCALE_RU,
                                              _SHORT_SCALE_RU, _HOUR,
                                              _MIN, _SEC)


def nice_number_ru(number, speech, denominators=range(1, 21)):
    """ Russian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 целых одна вторая" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """

    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        # Give up, just represent as a 3 decimal number
        return str(round(number, 3)).replace(".", ",")

    whole, num, den = result

    if not speech:
        if num == 0:
            return str(whole).replace(".", ",")
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    return_string = str()
    # first check some edge cases
    # fraction with own name - "половина" etc
    if whole == 0 and num == 1 and den <= 4:
        return '{}'.format(_SPECIAL_FRACTION_STRING_RU[den])

    # another edge case with special word
    if whole != 0 and num == 1 and den == 2:
        return '{} с половиной'.format(whole)

    # third case - "четверть"
    if den == 4:
        return '{}{} {}'.format(str(whole) + " и " if whole else "", num,
                                "четверть" if num == 1 else "четверти")

    # general case
    return_string += '{}'.format(str(whole) + " и " if whole != 0 else "")

    den_str = (_FRACTION_STRING_RU[den].singular
               if num == 1 else _FRACTION_STRING_RU[den].plural)
    return_string += '{} {}'.format(num, den_str)

    return return_string


def pronounce_number_ru(num, places=2, short_scale=True, scientific=False,
                        *, gender='masculine'):
    """
    Convert a number to its spoken equivalent

    For example, '5.2' would return 'пять целых две десятых'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
    Returns:
        (str): The pronounced number
    """
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:

            # This handles negatives of powers separately from the normal
            # handling since each call disables the scientific flag
            # TODO may be improve form later?
            return '{}{} на десять в степени {}{}'.format(
                'минус ' if float(n) < 0 else '',
                pronounce_number_ru(abs(float(n)), places, short_scale, False),
                'минус ' if power < 0 else '',
                pronounce_number_ru(abs(power), places, short_scale, False))

    if short_scale:
        number_names = _NUM_STRING_RU.copy()
        number_names.update(_SHORT_SCALE_RU)
        fractions = _FRACTION_STRING_RU.copy()
        fractions.update(_SHORT_SCALE_FRACTION_STRING_RU)
    else:
        number_names = _NUM_STRING_RU.copy()
        number_names.update(_LONG_SCALE_RU)
        fractions = _FRACTION_STRING_RU.copy()
        fractions.update(_LONG_SCALE_FRACTION_STRING_RU)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    hundreds = [number_names[n] for n in range(100, 1000, 100)]

    if short_scale:
        thousands = [_SHORT_SCALE_RU[n] for n in _SHORT_SCALE_RU.keys()]
    else:
        thousands = [_LONG_SCALE_RU[n] for n in _LONG_SCALE_RU.keys()]

    # deal with negatives
    result = ""
    if num < 0:
        result = "минус "
    num = abs(num)

    # check for a direct match
    if num in [digit.number for digit in digits + tens + hundreds]:
        result += number_names[int(num)].masculine if gender == 'masculine' \
            else number_names[int(num)].feminine

    elif num in [digit.number for digit in thousands]:
        result += ("одна {}" if num == 1000
                   else "один {}").format(number_names[int(num)].nomn)
    # check for overflowing
    elif int(num) > thousands[-1].number:
        result += " бесконечность"
    else:

        def _sub_thousand(n):
            assert 0 <= n <= 999
            if n <= 19:
                digits_list = [digits[n]]
            elif n <= 99:
                q, r = divmod(n, 10)
                digits_list = [tens[q - 1]]
                if r:
                    digits_list.extend(_sub_thousand(r))
            else:
                q, r = divmod(n, 100)
                digits_list = [hundreds[q - 1]]
                if r:
                    digits_list.extend(_sub_thousand(r))
            return digits_list

        def _short_scale(n):
            with_fraction = n != int(n) and places > 0

            n = int(n)
            assert 0 <= n <= thousands[-1].number
            num_list = []
            for i, z in enumerate(_split_by(n, 1000), -1):
                if z == 0:
                    continue
                num_str = ""
                subnum_list = _sub_thousand(z)
                for entity in subnum_list:

                    if i == 0 or (i == -1 and (with_fraction or
                                               gender == 'feminine')):
                        num_str += " " + entity.feminine
                    else:
                        num_str += " " + entity.masculine

                # order ending
                if i != -1:
                    if subnum_list[-1].number == 1:
                        num_str += " " + thousands[i].nomn
                    elif subnum_list[-1].number < 5:
                        num_str += " " + thousands[i].gen
                    else:
                        num_str += " " + thousands[i].gen_plur

                num_list.append(num_str.strip())

            if with_fraction:
                postfix = " целая" if n % 10 == 1 else " целых"
            else:
                postfix = ""

            return ", ".join(reversed(num_list)) + postfix

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _denum_str(n):
            order = 10 ** len(str(n))
            last_plural = True if n % 10 > 1 else False
            assert order <= 1e60  # max value in dict
            den_str = ""
            prefix = ""
            prefixes = ["стотысяче", "десятитысяче", "тысяче", "сто", "десяти"]
            while prefixes:
                if order in fractions:
                    den_str = fractions[order].plural if last_plural \
                        else fractions[order].singular
                    return prefix + den_str
                prefix = prefixes.pop()

                order -= 1

        def _long_scale(n):
            with_fraction = n != int(n) and places > 0
            n = int(n)
            assert 0 <= n <= thousands[-1].number
            res = []
            for i, z in enumerate(_split_by(n, 1000000), -1):
                if not z:
                    continue
                number = pronounce_number_ru(z, places, True, scientific)
                if i >= 0:
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    if z % 10 == 1:
                        thousand_name = thousands[i + 1].nomn
                    elif 1 < z % 10 < 5:
                        thousand_name = thousands[i + 1].gen
                    else:
                        thousand_name = thousands[i + 1].gen_plur
                    number += " " + thousand_name
                res.append(number)
            num_str = ", ".join(reversed(res))
            if with_fraction:
                num_str += " целая" if int(n) % 10 == 1 else " целых"
            return num_str

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

        # Deal with fractional part
        if num != int(num) and places > 0:
            fract = int(str(round(num, places)).split(".")[1])
            fract_num_str = pronounce_number_ru(fract, gender='feminine')
            fract_postfix = _denum_str(fract)
            result += ", " + fract_num_str + " " + fract_postfix

    return result


def nice_time_ru(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format

    For example, generate 'five thirty' for speech or '5:30' for
    text display.

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        speech (bool): format for speech (default/True) or display (False)=Fal
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
    Returns:
        (str): The formatted time string
    """
    if use_24hour:
        # e.g. "03:01" or "14:22"
        string = dt.strftime("%H:%M")
    else:
        if use_ampm:
            # e.g. "3:01 AM" or "2:22 PM"
            string = dt.strftime("%I:%M %p")
        else:
            # e.g. "3:01" or "2:22"
            string = dt.strftime("%I:%M")
        if string[0] == '0':
            string = string[1:]  # strip leading zeros

    if not speech:
        return string

    # Generate a speakable version of the time
    if use_24hour:
        speak = ""

        hour = int(string[1]) if string[0] == 0 else int(string[0:2])
        # special hours
        if hour == 1:
            speak += "час"
        else:
            speak += pronounce_number_ru(hour, gender='masculine')

        if string[3:5] == '00':
            speak += " ноль ноль"
        else:
            speak += " "
            if string[3] == "0":
                speak += "ноль "
                minute = int(string[4])
            else:
                minute = int(string[3:5])
            speak += pronounce_number_ru(minute, gender='feminine')
        if speak == "тринадцать две":
            __import__("pdb").set_trace()

        return speak
    else:
        hour_12 = dt.hour - 12 if dt.hour > 12 else dt.hour
        if dt.hour == 0 and dt.minute == 0 and not use_ampm:
            return "полночь"
        elif dt.hour == 12 and dt.minute == 0 and not use_ampm:
            return "полдень"
        elif dt.minute in [5, 10, 15] and not use_ampm:
            speak = pronounce_number_ru(dt.minute)
            speak += " минут " + _SPECIAL_TIME_RU[hour_12]
            return speak
        elif dt.minute in _SPECIAL_MIN_RU and not use_ampm:
            return _SPECIAL_MIN_RU[dt.minute] + " " + \
                pronounce_number_ru((hour_12 + 1) % 12)
        elif dt.minute == 30 and not use_ampm:
            return "половина " + _SPECIAL_TIME_RU[hour_12]
        elif dt.minute == 0 and not use_ampm:
            return "ровно " + pronounce_number_ru(hour_12) \
                if dt.hour not in [1, 13] else "ровно час"

        if dt.hour == 0:
            speak = pronounce_number_ru(12)
        elif dt.hour in [1, 13]:
            speak = "час"
        elif dt.hour < 13:
            speak = pronounce_number_ru(dt.hour)
        else:
            speak = pronounce_number_ru(dt.hour - 12)

        speak += " "
        if dt.minute < 10:
            speak += "ноль "
        speak += pronounce_number_ru(dt.minute, gender='feminine')

        if use_ampm:
            if dt.hour > 11:
                speak += " после полудня"
            else:
                speak += " до полудня"

        return speak
