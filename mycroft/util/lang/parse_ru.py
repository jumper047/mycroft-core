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
from datetime import timedelta  # datetime

import copy

# from dateutil.relativedelta import relativedelta

from mycroft.util.lang.parse_common import is_numeric  # , look_for_fractions
from mycroft.util.lang.common_data_ru import (
    _MINUS_RU, _FRACTION_MARKER_RU, _FRACTION_TO_NUM_RU, _ORDINAL_TO_NUM_RU,
    _STRING_TO_NUM_RU, _STRING_TO_TERM_RU)

import re

# _Token is intended to be used in the number processing functions in
# this module. The parsing requires slicing and dividing of the original
# text. To ensure things parse correctly, we need to know where text came
# from in the original input, hence this nametuple.
_Token = namedtuple('_Token', 'word index')

_SPECIAL_FRACTION_RU = {
    0.5: ["половина", "половиной", "половины", "половин"],
    0.333: ["треть", "трети", "третью", "третей"],
    0.25: ["четверть", "четверти", "четвертью", "четвертей"]
}


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
        terms = ru_numbers if not ordinals else ru_numbers_ordinals
        return word in terms and terms[word] > (1000 if short_scale else 1e9)


def _is_fraction(word):
    """Check if word is fraction"""

    return word in ru_fractions


def _is_special_fraction(word):

    return word in ru_special_fraction


# TODO add support for 3/4 etc


def _is_num_special_fraction(word):

    frac = word.split("/")
    return len(frac) == 2 and is_numeric(frac[0]) and is_numeric(frac[1])


def _is_plain_word(word):

    # TODO add more cases
    return not (_is_subthousand(word) or _is_term(word) or _is_fraction(word))


def _extract_integer_short_scale(tokens, ordinals=False):
    """Extract number from tokens (with short scale)"""

    result = 0
    tmp_result = 0
    for token in tokens:
        if _is_subthousand(token.word, True, ordinals):
            tmp_result += ru_numbers[
                token.word] if not ordinals else ru_numbers_ordinals[
                    token.word]
        elif _is_term(token.word, True, ordinals):
            result += (tmp_result * ru_terms[token.word]
                       ) if tmp_result != 0 else ru_terms[token.word]
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
        return _SPECIAL_FRACTION_RU[tokens[-1].word]
        # TODO add support for fractional parts > 20
    elif _is_fraction(tokens[-1].word):
        return _extract_integer(tokens[:-1], short_scale,
                                ordinals) / ru_fractions[tokens[-1].word]
    else:
        return 0


def _extract_tokens_with_numbers(tokens):

    tokens = tokens[:]
    placeholder = '<placeholder>'
    current_number = []
    numbers = []
    for index, token in enumerate(tokens):
        if _is_plain_word(token.word) and len(current_number) == 0:
            # continue going through plain text
            continue
        elif _is_plain_word(token.word) and len(current_number) > 0:
            # finalize word
            numbers.append(current_number)
            current_number = []
        else:
            # append token to number
            current_number.append(tokens.pop(index))
            tokens.insert(index, placeholder)
    return numbers


def _extract_number(tokens, short_scale, ordinals):

    tokens = list(tokens)
    negative = False
    integer = 0
    fraction = 0
    if tokens[0].word in _MINUS_RU:
        negative = True
        tokens = tokens[1:]
    words_list = [token.word for token in tokens]
    for marker in _FRACTION_MARKER_RU:
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
    tok_numbers = _extract_tokens_with_numbers(tokens)
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
    tok_numbers = _extract_tokens_with_numbers(tokens)
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


# def extract_datetime_en(string, dateNow, default_time):
#     """ Convert a human date reference into an exact datetime

#     Convert things like
#         "today"
#         "tomorrow afternoon"
#         "next Tuesday at 4pm"
#         "August 3rd"
#     into a datetime.  If a reference date is not provided, the current
#     local time is used.  Also consumes the words used to define the date
#     returning the remaining string.  For example, the string
#        "what is Tuesday's weather forecast"
#     returns the date for the forthcoming Tuesday relative to the reference
#     date and the remainder string
#        "what is weather forecast".

#     The "next" instance of a day or weekend is considered to be no earlier
#     than
#     48 hours in the future. On Friday, "next Monday" would be in 3 days.
#     On Saturday, "next Monday" would be in 9 days.

#     Args:
#         string (str): string containing date words
#         dateNow (datetime): A reference date/time for "tommorrow", etc
#         default_time (time): Time to set if no time was found in the string

#     Returns:
#         [datetime, str]: An array containing the datetime and the remaining
#                          text not consumed in the parsing, or None if no
#                          date or time related text was found.
#     """


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
