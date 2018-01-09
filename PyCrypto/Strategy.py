# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:09:10 2018

@author: npiro
"""

from scipy import stats
import datetime

def trend_stats(df, last_minutes = 30, window = 15, current_time = None, alpha = 0.01):
    """
    Compute trend statistics. 
    @df: Price dataframe
    @last_minutes: The number of minutes to compute stats from
    @window: the smoothing window size
    @current_time: the current datetime, as returned by datetime.datetime.now(). 
                   If not specified, it is obtained at function call
    Returns tuple of:
        the mean of the opening price, 
        the mean of the derivative,
        the standard error of the derivative,
        the t and p values of the derivative,
        trend: 1 if growing, -1 if falling
        is_significant: True if trend is statistically significant, False otherwise
        The statistically significant trend: Same as trend but 0 if no significant
    """
    if current_time is None:
        current_time = datetime.datetime.now()
    df_last_mins = df[(df['timestamp']>=current_time - datetime.timedelta(minutes=last_minutes)) & (df['timestamp']<current_time)].copy()
    der = df_last_mins['open'].diff()
    df_last_mins['derivative'] = der
    df_last_mins['open_sm'] = df_last_mins['open'].rolling(window = window, center = False).mean()
    #df_last_mins['derivative_sm'] = der.rolling(window = window, center = False).mean()
    df_last_mins['derivative_sm'] = df_last_mins['open_sm'].diff()
    der_mean = df_last_mins['derivative_sm'].mean()
    der_sem = df_last_mins['derivative_sm'].sem()
    open_mean = df_last_mins['open'].mean()

    x = df_last_mins.derivative_sm.values
    (t, p) = stats.ttest_1samp(x, 0, nan_policy='omit')
    #print('t-statistic = %6.3f pvalue = %6.4f' %  (t, p))
    trend = +1 if (t > 0) else -1 
    is_significant = (p < alpha)
    return (open_mean, der_mean, der_sem, t, p, trend, is_significant, trend*is_significant)
    
def decision(current, available, value_mean, der_mean, der_sem, t, p, 
             trend, is_significant, trend_significant, 
             buy_factor = 1, sell_factor = 1):
    """
    Implements the basic trading algorithm.
    If a statistically significant positive trend is observed: buy an amount
    proportional to the relative mean derivative and the available money
    If a statistically significant negative trend is observed: sell an amount
    proportional to the relative mean derivative and the available currency amount
    @current: the current amount of the currency available in wallet
    @available: the amount of source currency available for the trade
    @buy_factor: the proprotionality factor in the purchase calculation
    @sell_factor: the proportionality factor in the sell calculation
    Rest of parameters are as returned from trend_stats function
    
    Returns the amount of currenct to buy (positive value) or sell (negative value)
    """
    if trend_significant == 1:
        return available*buy_factor*der_mean/value_mean
    elif trend_significant == -1:
        return current*sell_factor*der_mean/value_mean
    else:
        return 0