#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff


def signal(*args):
    # QuanlityPriceCorr
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    df[factor_name] = df['close'].rolling(
        n).corr(df['quote_volume'])
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
