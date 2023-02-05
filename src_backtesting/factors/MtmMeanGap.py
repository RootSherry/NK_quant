#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps

# https://bbs.quantclass.cn/thread/18651

def signal(*args):
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['mtm'] = df['close'] / df['close'].shift(n) - 1

    df['_g']  = 1 - abs((df['close'] - df['open'])/(df['high'] - df['low'] + eps))
    df['gap'] = df['_g'].rolling(window=n, min_periods=1).mean()

    df[factor_name] = df['mtm'].rolling(window=n, min_periods=1).mean()/(df['gap'] + eps)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
