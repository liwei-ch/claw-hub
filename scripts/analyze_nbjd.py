#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析宁波精达(603088)
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("宁波精达(603088) 基本面/行情分析")
print("=" * 60)

# 获取实时行情
df = ak.stock_zh_a_spot()
row = df[df['代码'] == 'sh603088']
if not row.empty:
    print("\n1. 实时行情:")
    price = float(row.iloc[0]['最新价'])
    change = float(row.iloc[0]['涨跌幅'])
    print(f"  最新价: {price:.2f} 元")
    print(f"  涨跌幅: {change:.2f} %")
    print(f"  今开: {row.iloc[0]['今开']} 元")
    print(f"  最高: {row.iloc[0]['最高']} 元")
    print(f"  最低: {row.iloc[0]['最低']} 元")
    print(f"  昨收: {row.iloc[0]['昨收']} 元")
    print(f"  成交量: {int(row.iloc[0]['成交量'] / 10000):,} 万手")
    print(f"  成交额: {float(row.iloc[0]['成交额'] / 100000000):.2f} 亿元")

# 获取公司基本面
print("\n" + "=" * 60)
print("2. 基本面信息:")
try:
    info_df = ak.stock_individual_info_em(symbol="603088")
    print(info_df.to_string(index=False, header=False))
except Exception as e:
    print(f"获取基本面失败: {e}")

# 获取近期走势
print("\n" + "=" * 60)
print("3. 近期行情走势 (近10个交易日):")
try:
    kline_df = ak.stock_zh_a_daily(symbol="sh603088", start_date="20260301", end_date="20260316", adjust="qfq")
    kline_df = kline_df.sort_values('date', ascending=False).head(10)
    print(kline_df[['date', 'open', 'high', 'low', 'close', 'pct_chg', 'volume']].to_string(index=False))
except Exception as e:
    print(f"获取K线失败: {e}")

print("\n" + "=" * 60)
print("分析完成")
