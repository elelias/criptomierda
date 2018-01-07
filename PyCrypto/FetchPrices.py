# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 20:07:27 2018

@author: npiro
"""

import requests
import datetime
import pandas as pd

def price(symbol, comparison_symbols=['USD'], exchange=''):
    """
    Get price for symbol, compared to symbols in comparison_symbols
    @symbol: from currency
    @comparison_symbols: to currencies
    @exchange: name of exchange
    """

    url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'\
            .format(symbol.upper(), ','.join(comparison_symbols).upper())
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    return data

def daily_price_historical(symbol, comparison_symbol, all_data=True, limit=1, aggregate=1, exchange=''):
    """
    Get the daily aggregated price history of symbol compared to comparison_symbol
    @symbol: from currency
    @comparison_symbol: to_currency
    @all_date: whether to fetch all available data
    @limit: how many periods to fetch
    @aggregate: how many periods to aggregate (average)
    @exchange: name of exchange
    """
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df


def hourly_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    """
    Get the hourly aggregated price history of symbol compared to comparison_symbol
    @symbol: from currency
    @comparison_symbol: to_currency
    @all_date: whether to fetch all available data
    @limit: how many periods to fetch
    @aggregate: how many periods to aggregate (average)
    @exchange: name of exchange
    """
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df


def minute_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    """
    Get the minute aggregated price history of symbol compared to comparison_symbol
    @symbol: from currency
    @comparison_symbol: to_currency
    @all_date: whether to fetch all available data
    @limit: how many periods to fetch
    @aggregate: how many periods to aggregate (average)
    @exchange: name of exchange
    """
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df