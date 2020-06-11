# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import requests
import re
import json
from . import macro_replacement_fields
from decimal import Decimal
from superdesk.cache import cache
from flask import current_app as app


RATE_SERVICE = 'http://data.fixer.io/api/latest?access_key={}&symbols={}'
SUFFIX_REGEX = r'((\s*\-?\s*)((mln)|(bln)|(bn)|([mM]illion)|([bB]illion)|[mb]))?\)?'
SECONDARY_SUFFIX_REGEX = r'(\s*\-?\s*)((mln)|(bln)|(bn)|([mM]illion)|([bB]illion)|[mb])?\)?'
SYMBOLS = 'USD,AUD,CHF,NZD,CNY,GBP,EUR,JPY'


def to_currency(value, places=2, curr='', sep=',', dp='.', pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    if places:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


@cache(ttl=43200)
def get_all_rates():
    r = requests.get(RATE_SERVICE.format(app.config.get('CURRENCY_API_KEY', ''), SYMBOLS), timeout=5)
    r.raise_for_status()
    result = json.loads(r.text)
    if result.get('success') is True:
        return result
    else:
        raise LookupError('Failed to retrieve currency conversion rates')


def get_rate(from_currency, to_currency):
    """Get the exchange rate."""
    result = get_all_rates()
    if result.get('success') is True:
        from_value = result.get('rates').get(from_currency)
        to_value = result.get('rates').get(to_currency)
    else:
        raise LookupError('Failed to retrieve currency conversion rate')

    return Decimal(to_value / from_value)


def update_suffix(value, suffix, precision=0):
    """Updates the
    :param value:
    :param suffix:
    :param precision:
    :return:
    """
    thousand = Decimal(1000)
    million = Decimal(1000000)
    billion = Decimal(1000000000)
    trillion = Decimal(1000000000000)
    million_suffixes = ['m', 'mln', 'million']
    billion_suffixes = ['b', 'bln', 'billion']

    if not suffix:
        if value >= trillion:
            value = value / trillion
            suffix = 'trillion'
        if value >= billion:
            value = value / billion
            suffix = 'billion'
        if value >= million:
            value = value / million
            suffix = 'million'

    if (value >= thousand) and suffix in billion_suffixes:
        value = value / thousand
        suffix = 'trillion'

    if (value >= thousand) and suffix in million_suffixes:
        value = value / thousand
        suffix = 'billion'

    if precision == 0:
        if value < Decimal(1):
            precision = 2
        elif value < Decimal(10):
            precision = 1

    return value, suffix, precision


def format_output(original, converted, suffix, src_currency):
    """Returns the replacement string for the given original value"""
    original = original if src_currency is None or src_currency in original \
        else original.replace('$', src_currency)
    if suffix:
        return '{} ({} {})'.format(original, converted, suffix)
    else:
        return '{} ({})'.format(original, converted)


def do_conversion(item, rate, currency, search_param, match_index, value_index, suffix_index, src_currency=None):
    """
    Performs the conversion
    :param item: story
    :param rate: exchange rate
    :param currency: currency symbol or prefix to be used in the results
    :param search_param: search parameter to locate the original value.  It should
    be a valid regular expression pattern, and not just an arbitrary string.
    :param match_index: int index of groups used in matching string
    :param value_index: int index of groups used in converting the value
    :param suffix_index: int index of groups used for millions or billions
    :return: modified story
    """
    diff = {}

    def convert(match):
        match_item = match.group(match_index)
        value_item = match.group(value_index)
        suffix_item = match.group(suffix_index)
        if match_item and value_item:
            if ')' in match_item and '(' not in match_item:
                # clear any trailing parenthesis
                match_item = re.sub('[)]', '', match_item)

            from_value = Decimal(re.sub(r'[^\d.]', '', value_item))
            precision = abs(from_value.as_tuple().exponent)
            to_value = rate * from_value
            to_value, suffix_item, precision = update_suffix(to_value, suffix_item, precision)
            converted_value = to_currency(to_value, places=precision, curr=currency)
            diff.setdefault(match_item, format_output(match_item, converted_value, suffix_item, src_currency))
            return diff[match_item]

    # if the rate is returned from the cache it's type will be float, we need to change it to Decimal
    if isinstance(rate, float):
        rate = Decimal(rate)

    for field in macro_replacement_fields:
        if item.get(field, None):
            re.sub(search_param, convert, item[field])

    return (item, diff)
