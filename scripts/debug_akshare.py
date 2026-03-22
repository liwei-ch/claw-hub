#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试AkShare接口，查看返回数据结构
"""

import akshare as ak
import pandas as pd

print("查看stock_zh_a_spot返回列名:")
df = ak.stock_zh_a_spot()
print("\n列名:", list(df.columns))
print("\n前2行数据:")
print(df.head(2))
print("\n数据形状:", df.shape)
