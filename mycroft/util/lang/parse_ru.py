# -*- coding: utf-8 -*-
#
# Copyright 2017 Mycroft AI Inc.
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
from collections import namedtuple
from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta

import copy

# from dateutil.relativedelta import relativedelta

from mycroft.util.lang.parse_common import is_numeric  # , look_for_fractions
from mycroft.util.lang.common_data_ru import (
    _MINUS_RU, _FRACTION_MARKER_RU, _FRACTION_TO_NUM_RU, _ORDINAL_TO_NUM_RU,
    _STRING_TO_NUM_RU, _STRING_TO_TERM_RU, _SPECIAL_FRACTION_RU, _MAYBE_FRACTION_MARKER_RU)

import re

# _Token is intended to be used in the number processing functions in
# this module. The parsing requires slicing and dividing of the original
# text. To ensure things parse correctly, we need to know where text came
# from in the original input, hence this nametuple.
_Token = namedtuple('_Token', 'word index')


def _revert_dict(dictionary):
    result = dict()
    for k in dictionary:
        for v in dictionary[k]:
            result[v] = k
    return result


ru_numbers = _revert_dict(_STRING_TO_NUM_RU)
ru_terms = _revert_dict(_STRING_TO_TERM_RU)
ru_fractions = _revert_dict(_FRACTION_TO_NUM_RU)
ru_special_fraction = _revert_dict(_SPECIAL_FRACTION_RU)
ru_ordinals = _revert_dict(_ORDINAL_TO_NUM_RU)
ru_numbers_ordinals = copy.copy(ru_numbers)
ru_numbers_ordinals.update(ru_ordinals)


def _tokenize(text):
    """
    Generate a list of token object, given a string.
    Args:
        text str: Text to tokenize.

    Returns:
        [_Token]

    """
    return [_Token(word, index) for index, word in enumerate(text.split())]


def _is_subthousand(word, short_scale=True, ordinals=False):
    """Check if word is integer less than 1000"""

    if is_numeric(word):
        return float(word) < (1000 if short_scale else 1e6)
    else:
        integers = ru_numbers if not ordinals else ru_numbers_ordinals
        return word in integers and integers[word] < (1000
                                                      if short_scale else 1e6)


def _is_term(word, short_scale=True, ordinals=False):
    """Check if word is term"""

    # term can't be a float
    if is_numeric(word):
        return False
    else:
        return word in ru_terms and ru_terms[word] > (1000 if short_scale else 1e9)


def _is_fraction(word):
    """Check if word is fraction"""

    return word in ru_fractions


def _is_special_fraction(word):

    return word in ru_special_fraction


# TODO add support for 3/4 etc


def _is_num_special_fraction(word):

    frac = word.split("/")
    return len(frac) == 2 and is_numeric(frac[0]) and is_numeric(frac[1])


def _is_plain_word(word, ordinals=False):

    # TODO add more cases
    return not (_is_subthousand(word, ordinals=ordinals) or _is_term(word) or _is_fraction(word) or
                _is_special_fraction(word) or _is_num_special_fraction(word) or
                word in _FRACTION_MARKER_RU)


def _different_numbers(word1, word2, short_scale=True, ordinals=False):

    if not _is_subthousand(word1) or not _is_subthousand(word2):
        return False

    if is_numeric(word1):
        num1 = int(word1)
    else:
        num1 = ru_numbers[word1] if ordinals else ru_numbers_ordinals[word1]
    if is_numeric(word2):
        num2 = int(word2)
    else:
        num2 = ru_numbers[word2] if ordinals else ru_numbers_ordinals[word2]
    return num1 < 20 or len(str(num1)) <= len(str(num2))


def _is_special_fraction_marker(word_left, word, word_right):

    return (word in _MAYBE_FRACTION_MARKER_RU and (_is_subthousand(word_left) or _is_term(word_left) or is_numeric(word_left)) and (_is_subthousand(word_right) or _is_term(word_right) or _is_special_fraction(word_right) or is_numeric(word_right)))


def _extract_integer_short_scale(tokens, ordinals=False):
    """Extract number from tokens (with short scale)"""

    result = 0
    tmp_result = 0
    for token in tokens:
        if _is_subthousand(token.word, True, ordinals):
            if is_numeric(token.word):
                tmp_result += int(token.word)
            elif not ordinals:
                tmp_result += ru_numbers[token.word]
            else:
                tmp_result += ru_numbers_ordinals[token.word]
        elif _is_term(token.word, True, ordinals):
            if is_numeric(token.word):
                num = int(token.word)
            else:
                num = ru_terms[token.word]
            result += (tmp_result * num
                       ) if tmp_result != 0 else num
            tmp_result = 0
    result += tmp_result
    return result


def _extract_integer_long_scale(tokens, ordinals=False):
    """Extract number from tokens (with long scale)

    Due to current state of russian language, there is no need in this function
    so it just return short scale int"""

    return _extract_integer_short_scale(tokens)


def _extract_integer(tokens, short_scale=True, ordinals=False):
    """Extract integer from list of tokens"""

    if short_scale:
        return _extract_integer_short_scale(tokens, ordinals)
    else:
        return _extract_integer_long_scale(tokens, ordinals)


def _extract_fraction(tokens, short_scale=True, ordinals=False):
    """Extract fraction number from tokens"""

    # edge case - "с половиной" etc
    if _is_special_fraction(tokens[-1].word):
        return ru_special_fraction[tokens[-1].word]
        # TODO add support for fractional parts > 20
    elif _is_fraction(tokens[-1].word):
        return _extract_integer(tokens[:-1], short_scale,
                                ordinals) / ru_fractions[tokens[-1].word]
    else:
        return 0


def _extract_tokens_with_numbers(tokens, ordinals=False):

    tokens = tokens[:]
    placeholder = '<placeholder>'
    current_number = []
    numbers = []
    for index, token in enumerate(tokens):
        if _is_plain_word(token.word, ordinals=ordinals) and len(current_number) == 0:
            # continue going through plain text
            continue
        elif token.word in _MAYBE_FRACTION_MARKER_RU and len(current_number) > 0:
            if (0 < index < len(tokens) - 1) and _is_special_fraction_marker(tokens[index-1].word, token.word, tokens[index+1].word):
                current_number.append(token)
            else:
                numbers.append(current_number)
                current_number = []
        elif _is_plain_word(token.word, ordinals=ordinals) and len(current_number):
            # finalize word
            numbers.append(current_number)
            current_number = []
        elif index > 0 and _different_numbers(tokens[index-1].word, token.word):
            numbers.append(current_number)
            current_number = [token]
        else:
            # append token to number
            # current_number.append(tokens.pop(index))
            # tokens.insert(index, placeholder)
            current_number.append(token)
    if len(current_number):
        numbers.append(current_number)
    return numbers


def _extract_number(tokens, short_scale, ordinals):

    tokens = list(tokens)
    negative = False
    integer = 0
    fraction = 0
    if len(tokens) == 0:
        return None
    if tokens[0].word in _MINUS_RU:
        negative = True
        tokens = tokens[1:]
    words_list = [token.word for token in tokens]
    fract = list(_FRACTION_MARKER_RU)
    fract += _MAYBE_FRACTION_MARKER_RU
    for marker in fract:
        try:
            marker_index = words_list.index(marker)
            integer = _extract_integer(tokens[:marker_index], short_scale,
                                       ordinals)
            fraction = _extract_fraction(tokens[marker_index + 1:],
                                         short_scale, ordinals)
            break
        except ValueError:
            continue
    else:
        fraction = _extract_fraction(tokens, short_scale, ordinals)
        if fraction == 0:
            integer = _extract_integer(tokens, short_scale, ordinals)
    result = integer + fraction
    if negative:
        result *= -1
    return result


def extractnumber_ru(text, short_scale=True, ordinals=False):
    """
    This function extracts a number from a text string,
    handles pronunciations in long scale and short scale

    https://en.wikipedia.org/wiki/Names_of_large_numbers

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found
    """
    tokens = _tokenize(text)
    tok_numbers = _extract_tokens_with_numbers(tokens, ordinals)
    if len(tok_numbers) == 0:
        return False
    else:
        return _extract_number(tok_numbers[0], short_scale, ordinals)


def extract_numbers_ru(text, short_scale=True, ordinals=False):
    """
        Takes in a string and extracts a list of numbers.

    Args:
        text (str): the string to extract a number from
        short_scale (bool): Use "short scale" or "long scale" for large
            numbers -- over a million.  The default is short scale, which
            is now common in most English speaking countries.
            See https://en.wikipedia.org/wiki/Names_of_large_numbers
        ordinals (bool): consider ordinal numbers, e.g. third=3 instead of 1/3
    Returns:
        list: list of extracted numbers as floats
    """

    tokens = _tokenize(text)
    tok_numbers = _extract_tokens_with_numbers(tokens, ordinals)
    if len(tok_numbers) == 0:
        return False
    else:
        return [
            _extract_number(number, short_scale, ordinals)
            for number in tok_numbers
        ]


def extract_duration_ru(text):
    """
    Convert an english phrase into a number of seconds

    Convert things like:
        "10 минут"
        "2 часа и пол минуты"
        "3 дня 8 часов 10 минут и 49 секунд"
    into an int, representing the total number of seconds.

    The words used in the duration will be consumed, and
    the remainder returned.

    As an example, "set a timer for 5 minutes" would return
    (300, "set a timer for").

    Args:
        text (str): string containing a duration

    Returns:
        (timedelta, str):
                    A tuple containing the duration and the remaining text
                    not consumed in the parsing. The first value will
                    be None if no duration is found. The text returned
                    will have whitespace stripped from the ends.
    """
    if not text:
        return None

    time_units = {
        'microseconds': None,
        'milliseconds': None,
        'seconds': None,
        'minutes': None,
        'hours': None,
        'days': None,
        'weeks': None
    }

    time_words_ru = {
        'microseconds': ['микросекунд'],
        'milliseconds': ['миллисекунд'],
        'secnods': ['секунд'],
        'hours': ['час'],
        'days': ['день', 'дня', 'дней'],
        'weeks': ['недел']
    }
    ru_time_words = _revert_dict(time_words_ru)
    tokens = _tokenize(text)
    num_tokens = []
    rest = []
    for t in tokens:
        if not _is_plain_word(t.word):
            num_tokens.append(t)
        elif t.word in ru_time_words:
            number = extractnumber_ru(' '.join(t.word for t in num_tokens))
            if number is not False:
                time_units[time_words_ru[t.word]] = number
            num_tokens = []
        else:
            rest.append(t)
    duration = timedelta(**time_units) if any(time_units.values()) else None

    return (duration, ' '.join([t.word for t in rest]))

# через спустя


def _extract_now(words, current_dt):

    offset = {
        'microseconds': 0,
        'milliseconds': 0,
        'seconds': 0,
        'minutes': 0,
        'hours': 0,
        'days': 0,
        'weeks': 0,
        'years': 0
    }

    if "сейчас" in words:
        return (offset, [words.index("сейчас")], True)
    else:
        return None


def _extract_absolute_date(words, current_dt):
    # 3е декабря

    months = {1: ["январь", "января", "январе", "январю"],
              2: ["февраль", "февраля", "феврале", "февралю"],
              3: ["март", "марта", "марте", "марту"],
              4: ["апрель", "апреля", "апреле", "апрелю"],
              5: ["май", "мая", "мае", "маю"],
              6: ["июнь","июня","июне","июню"],
              7: ["июль","июля","июле","июлю"],
              8: ["август", "августа","августе","августу",],
              9: ["сентябрь", "сентября", "сентябре", "сентябрю"],
              10: ["октябрь", "октября", "октябре", "октябрю"],
              11: ["ноябрь", "ноября", "ноябре", "ноябрю"],
              12: ["декабрь", "декабря", "декабре", "декабрю"]}

    months_r = _revert_dict(months)

    # normalize numbers
    norm_words = []
    for word in words:
        if len(word) > 1 and is_numeric(word[0]) and word[-1] in ['о', 'е', 'у']:
            num = ""
            for letter in word:
                if is_numeric(letter):
                    num += letter
            norm_words.append(num)
        else:
            norm_words.append(word)
    
    parsed_positions = []
    offset = dict()
    day = month = year = None
    for num, word in enumerate(norm_words):
        if word in months_r:
            # check if it is day before
            parsed_positions.append(num)
            month = months_r[word]
            if num > 0 and _is_subthousand(norm_words[num-1]):
                day_txt = norm_words[num-1]
                parsed_positions.append(num-1)
                if num > 1 and _is_subthousand(norm_words[num-2]):
                    # check if it is part of one number
                    if _is_subthousand(norm_words[num-2]) and not _different_numbers(words[num-2], word[num-1], ordinals=True) and extractnumber_ru(" ".join((words[num-2], words[num-1]))) <= 31:
                        day_txt += " " + norm_words[num-2]
                        parsed_positions.append(num-2)
                day = extractnumber_ru(day_txt)
            # check if it is a full year after
            # first check numeric year
            if len(norm_words) > num + 1 and is_numeric(norm_words[num+1]) and len(norm_words[num+1]) == 4:
                year = extractnumber_ru(norm_words[num+1])
                parsed_positions.append(num + 1)
            break
    else:
        return None


    cur_year=int(current_dt.strftime("%Y"))
    cur_month=int(current_dt.strftime("%m"))
    cur_day=int(current_dt.strftime("%d"))
    
    print("parsed:", year, month, day, "curr", cur_year, cur_month, cur_day)
    if year is not None:
        offset['years'] = year - cur_year
    if day is not None:
        offset['days'] = day - cur_day
    offset['months'] = month - cur_month

    return (offset, parsed_positions, False)

    


def _extract_interval(words, current_dt):

    interval_markers = ['через', 'спустя', 'подожди']
    parsed_positions = []
    norm_words = []

    # replace some words peculiar to intervals
    for word in words:
        if word in ["пара", "пару"]:
            norm_words.append("2")
        elif word == 'пол':
            norm_words.append("половина")
        else:
            norm_words.append(word)

    for marker in interval_markers:
        if marker in norm_words:
            parsed_positions.append(norm_words.index(marker))
            break
    else:
        return None

    enough = False

    offset = dict()

    time_words = {
        'microseconds': ['микросекунд', 'микросекунду', 'микросекунд'],
        'milliseconds': ['миллисекунды', 'миллисекунду', 'миллисекунд'],
        'seconds': ['секунду', 'секунды', 'секунд'],
        'minutes': ['минуту', 'минут', 'минуты'],
        'hours': ['час', 'часа', 'часов'],
        'days': ['день', 'дня', 'дней'],
        'weeks': ['недель', 'недели', 'неделю'],
        'months': ['месяцев', 'месяца', 'месяц'],
        'years': ['год', 'года', 'лет'],
        'decade': ['десятилетие', 'десятилетия', 'десятилетий'],
        'century': ['столетие', 'столетия', 'столетий'],
        'millenium': ['тысячелетие', 'тысячелетия', 'тысячелетий']
    }

    time_words_r = _revert_dict(time_words)

    last_index = 0
    prev_time_word = 0

    for index, word in enumerate(norm_words):
        if word in time_words_r:
            last_index = index
            parsed_positions.append(index)
            number_words = []
            for rev_idx in range(index - 1, prev_time_word, -1):
                if not _is_plain_word(norm_words[rev_idx]):
                    number_words.append(norm_words[rev_idx])
                    parsed_positions.append(rev_idx)
            # remove "и" between terms
            if len(words) > prev_time_word + 2 and words[prev_time_word + 1] == "и":
                parsed_positions.append(prev_time_word + 1)

            number = extractnumber_ru(" ".join(number_words))

            if number is False:
                number = 1

            if time_words_r[word] == 'decade':
                offset['years'] = offset.get('years', 0) + number * 10
            elif time_words_r[word] == 'century':
                offset['years'] = offset.get('years', 0) + number * 100
            elif time_words_r[word] == 'millenium':
                offset['years'] = offset.get('years', 0) + number * 1000
            elif time_words_r[word] == 'minutes':
                offset['seconds'] = offset.get('seconds', 0) + number * 60
            else:
                offset[time_words_r[word]] = offset.get(time_words_r[word], 0) + number
            prev_time_word = index


    if len(norm_words) > last_index + 1 and norm_words[last_index + 1] == 'после':
        parsed_positions.append(last_index + 1)
    else:
        enough = True

    return (offset, parsed_positions, enough)

def _extract_next_term(words, current_dt):

    offset = dict()
    next_word = ['следующее', 'следующий', 'следующем', 'следующей']
    prev_word = ['прошлый', 'прошлое', 'прошлая', 'прошлую', 'прошлые', 'том', 'той', 'та', 'тот', 'тех']
    time_words = {
        'microseconds': ['микросекунда', 'микросекунду', 'микросекунд','микросекунда'],
        'milliseconds': ['миллисекунды', 'миллисекунду', 'миллисекунда', 'миллисекунд'],
        'seconds': ['секунду', 'секунды', 'секунд', 'секунда'],
        'minutes': ['минуту', 'минут', 'минуты','минута'],
        'hours': ['час', 'часа', 'часов', 'часу'],
        'days': ['день', 'дня', 'дней', 'час'],
        'weeks': ['недель', 'недели', 'неделю', 'неделя', 'неделе'],
        'months': ['месяцев', 'месяца', 'месяц', 'месяцу', 'месяце'],
        'years': ['год', 'года', 'лет', 'году'],
        'decade': ['десятилетие', 'десятилетия', 'десятилетий', 'десятилетии'],
        'century': ['столетие', 'столетия', 'столетий', 'столетии'],
        'millenium': ['тысячелетие', 'тысячелетия', 'тысячелетий', 'тысячелетии']
    }

    time_words_r = _revert_dict(time_words)

    for num, word in enumerate(words):
        if word in next_word and len(words) > num + 1 and words[num+1] in time_words_r:
            nword = words[num+1]
            if time_words_r[nword] == 'decade':
                offset['years'] = 10
            elif time_words_r[nword] == 'century':
                offset['years'] = 100
            elif time_words_r[nword] == 'millenium':
                offset['years'] = 1000
            elif time_words_r[nword] == 'minutes':
                offset['seconds'] = 60
            else:
                offset[time_words_r[nword]] = 1
            return (offset, [num, num + 1], False)

        elif word in prev_word and len(words) > num and words[num+1] in time_words_r:
            nword = words[num+1]
            if time_words_r[nword] not in ['weeks', 'years', 'decade',
                                           'century', 'millenium']:
                return None
            nword = words[num+1]
            if time_words_r[nword] == 'decade':
                offset['years'] = -10
            elif time_words_r[nword] == 'century':
                offset['years'] = -100
            elif time_words_r[nword] == 'millenium':
                offset['years'] = -1000
            else:
                offset[time_words_r[nword]] = -1


            return (offset, [num, num + 1], False)
    return None


def _extract_weekday(words, current_dt):

    weekdays = {1: ["понедельник", "понедельника", "понедельнику"],
                2: ["вторник", "вторника", "вторнику"],
                3: ["среда", "среду", "среды"],
                4: ["четверг", "четверга", "четвергу"],
                5: ["пятница", "пятницу", "пятницы"],
                6: ["суббота", "субботу", "субботы"],
                7: ["воскресенье", "воскресенья", "воскресенью"]}

    offsets = {-2: ["позапрошлый", "позапрошлого", "позапрошлому", "позапрошлой"],
               -1: ["прошлый", "прошлого", "прошлому", "прошлой"],
               0: ["этот"],
               1: ["следующий", "следующая", "следующую", "следующей", "следующего"]}

    weekdays_r = _revert_dict(weekdays)
    offsets_r = _revert_dict(offsets)

    if not set(weekdays_r).intersection(set(words)):
        return None
    
    for num, word in enumerate(words):
        if word in weekdays_r:
            current_day = int(current_dt.strftime('%w'))
            parsed_day = weekdays_r[word]
            days_offset = parsed_day - current_day
            if num > 0 and words[num-1] in offsets_r:
                week_offset = offsets_r[words[num-1]]
            else:
                week_offset = None
            break
    
    if week_offset is None:
        if days_offset < 0:
            days_offset += 7
        return ({'days': days_offset}, [num], False)
    else:
        print(num, days_offset, week_offset, "seems like we parsing next word")
        # days_offset += 7 * week_offset
        return ({'days': days_offset, 'weeks': week_offset}, [num-1, num], False)
    

def _extract_relative_day(words, current_dt):
    offsets = {"позавчера": -2,
               "вчера": -1,
               "сегодня": 0,
               "завтра": 1,
               "послезавтра": 2}

    for num, word in enumerate(words):
        if word in offsets:
            return ({'days': offsets[word]}, [num], False) 
    return None

def _extract_pronoun_time(tokens):
    # двадцать часов пятнадцать минут
    pass

def _time_to_offset(parsed_dt, current_dt):
    if parsed_dt > current_dt:
        delta = parsed_dt - current_dt
        minus = False
    else:
        delta = current_dt - parsed_dt
        minus = True
    hours, seconds = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if minus:
        hours *= -1
        minutes *= -1
    return {'hours': hours,'minutes': minutes, 'seconds': seconds}


def _extract_short_pron_time(words, current_dt):

    preamble_words = ['в', 'на']

    for num, word in enumerate(words):
        parsed_positions = []
        hour = minute = 0
        next_word = words[num+1] if num + 1 < len(words) else ""
        next_next_word = words[num+2] if num + 2 < len(words) else ""
        hour = extractnumber_ru(word)
        if hour is not False and not 0<=hour<=23:
            continue
        parsed_positions.append(num)
        
        minute1 = extractnumber_ru(next_word)
        minute2 = extractnumber_ru(next_next_word)
        if minute1 is not False and minute2 is not False and minute1 == 0 and 0 <= minute2 <= 9:
            minute = minute2
            parsed_positions.extend([num+1, num+2])
        elif 10 <= minute1 <= 19:
            minute = minute1
            parsed_positions.append(num+1)
        elif 20 <= minute1 <=50 and minute2 and 1 <= minute2 <= 9:
            minute = minute1 + minute2
            parsed_positions.extend([num+1, num+2])
        else:
            continue
        if num > 0 and words[num-1] in preamble_words:
            parsed_positions.append(num-1)
        parsed_time = current_dt.replace(hour=hour, minute=minute) 
        offset = _time_to_offset(parsed_time, current_dt)
        return (offset, parsed_positions, True)

def _extract_short_pronoun_time(tokens):
    # пять [пятнадцать] [утра]
    pass


def _extract_numeric_time(words, current_dt):
    # 15:25
    
    preamble_words = ['в', 'на']
    parsed_positions = []

    for num, word in enumerate(words):
        try:
            hours, minutes = word.split(":")
            hours = int(hours)
            minutes = int(minutes)
        except ValueError:
            continue
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            break
    else:
        return None
    parsed_time = current_dt.replace(hour=hours, minute=minutes)
    offset = _time_to_offset(parsed_time, current_dt)
    parsed_positions.append(num)
    if num > 0 and words[num-1] in preamble_words:
        parsed_positions.append(num-1)
    return(offset, parsed_positions, True)

def _extract_daytime(words, current_dt):

    daytimes = {8: ['утро', 'утром', 'утру'],
                12: ['полдень', 'полудню'],
                15: ['обед', 'обеду', 'обеда'],
                19: ['вечером', 'вечеру', 'вечер'],
                0: ['полночь', 'полуночи']}
    
    preamble_words = ['в', 'к', 'после', 'этот', 'этим']
    prepreamble_words = ['точно', 'ровно']

    daytimes_r = _revert_dict(daytimes)

    for num, word in enumerate(words):
        if word in daytimes_r:
            parsed_positions = [num]
            parsed_time = current_dt.replace(hour=daytimes_r[word], minute=0)
            offset = _time_to_offset(parsed_time, current_dt)
            if num > 0 and words[num-1] in preamble_words:
                parsed_positions.append(num-1)
                if num > 1 and words[num-2] in prepreamble_words:
                    parsed_positions.append(num-2)
            return (offset, parsed_positions, True)

def extract_datetime_ru(string, date_now, default_time):
    """ Convert a human date reference into an exact datetime

    Convert things like
        "today"
        "tomorrow afternoon"
        "next Tuesday at 4pm"
        "August 3rd"
    into a datetime.  If a reference date is not provided, the current
    local time is used.  Also consumes the words used to define the date
    returning the remaining string.  For example, the string
       "what is Tuesday's weather forecast"
    returns the date for the forthcoming Tuesday relative to the reference
    date and the remainder string
       "what is weather forecast".

    The "next" instance of a day or weekend is considered to be no earlier
    than
    48 hours in the future. On Friday, "next Monday" would be in 3 days.
    On Saturday, "next Monday" would be in 9 days.

    Args:
        string (str): string containing date words
        dateNow (datetime): A reference date/time for "tommorrow", etc
        default_time (time): Time to set if no time was found in the string

     Returns:
         [datetime, str]: An array containing the datetime and the remaining
                          text not consumed in the parsing, or None if no
                          date or time related text was found.
    """

    words = string.split()

    offset = {
        'microseconds': None,
        'milliseconds': None,
        'seconds': None,
        'minutes': None,
        'hours': None,
        'days': None,
        'weeks': None,
        'months': None,
        'years': None
    }

    def update_offset(off):
        nonlocal offset
        print(offset, off)
        for t in offset:
            print(t)
            if t not in off:
                print(t, "not in off")
                continue
            if offset[t] is not None:
                offset[t] += off[t]
            else:
                offset[t] = off[t]

    def strip_words(numbers):
        nonlocal words
        words = [word for ind, word in enumerate(words) if ind not in numbers]

    def calculate_dt():
        nonlocal date_now, offset
        print(offset)
        years = offset['years']
        months = offset['months']
        delta_args_pos = {name: value for name,
                          value in offset.items() if name not in ['years', 'months']
                          and value != None and value > 0}
        result = date_now + timedelta(**delta_args_pos)
        print(delta_args_pos)
        print(result)
        delta_args_neg = {name: -value for name,
                          value in offset.items() if name not in ['years', 'months']
                          and value != None and value < 0}
        result = result - timedelta(**delta_args_neg)
        print(delta_args_neg)
        print(result)
        if years is not None:
            if years > 0:
                result += relativedelta(years=years)
            else:
                result -= relativedelta(years=abs(years))
        if months is not None:
            if months > 0:
                result += relativedelta(months=months)
            else:
                result -= relativedelta(months=abs(months))
        return result

    extractors = [_extract_now, _extract_interval, _extract_next_term,
                  _extract_weekday, _extract_relative_day,_extract_absolute_date, _extract_short_pron_time, _extract_numeric_time,
                  _extract_daytime]
    for function in extractors:
        result = function(words, date_now)
        if result is not None:
            update_offset(result[0])
            strip_words(result[1])
            print("offset became", offset)
            print("words rest became", words)
            if result[2]:
                break
    result = calculate_dt()
    times = ['microseconds',
            #  'milliseconds',
             'seconds',
             'minutes',
             'hours']
    time_set = len([offset[value] for value in times if offset[value] is not None]) != 0
    if not time_set:
        for interval in times:
            if offset[interval] is None:
                result = result.replace(**{interval[:-1]: 0})

    if default_time is not None and not time_set:
        result = result.replace(hour=default_time.hour,
                       minute=default_time.minute, second=default_time.second)
    return [result, " ".join(words)]

def normalize_ru(text, remove_articles=True):
    """
        Russian string normalization

    Args:
        test (str): text to normalize
        remove_articles (bool): meaningless due to lack of articles
             in russian.
    """

    # remove punctuation
    text = re.sub(r'-|\?|\!|\.|\,', '', text).lower()
    words = text.split()
    normalized = []
    for word in words:
        # Convert numbers into digits, e.g. "два" -> "2"
        for num_word, number in ru_numbers.items():
            if word == num_word and ru_numbers[num_word] < 21:
                normalized.append(str(number))
                break
        else:
            normalized.append(word)

    return ' '.join(normalized)
