#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取2026-03-16午后大盘行情
"""

import akshare as ak
import pandas as pd
from datetime import datetime

print("=" * 60)
print("2026年3月16日 午后大盘行情分析")
print("获取时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 获取全部行情数据
df = ak.stock_zh_a_spot()

# 统计全市场涨跌
print("\n1. 全市场涨跌统计:")
df_stock = df.copy()
# 筛选6位数字代码的A股
df_stock = df_stock[df_stock['代码'].str.match(r'^\d{6}$')]
df_stock['涨跌幅_num'] = pd.to_numeric(df_stock['涨跌幅'], errors='coerce')
df_stock = df_stock.dropna(subset=['涨跌幅_num'])

up = len(df_stock[df_stock['涨跌幅_num'] > 0])
down = len(df_stock[df_stock['涨跌幅_num'] < 0])
flat = len(df_stock[df_stock['涨跌幅_num'] == 0])
total = len(df_stock)

limit_up = len(df_stock[df_stock['涨跌幅_num'] >= 9.5])
limit_down = len(df_stock[df_stock['涨跌幅_num'] <= -9.5])

more_3 = len(df_stock[df_stock['涨跌幅_num'] > 3])
more_5 = len(df_stock[df_stock['涨跌幅_num'] > 5])
less_3 = len(df_stock[df_stock['涨跌幅_num'] < -3])
less_5 = len(df_stock[df_stock['涨跌幅_num'] < -5])

up_ratio = up / total * 100

print(f"  上涨家数: {up}")
print(f"  下跌家数: {down}")
print(f"  平盘家数: {flat}")
print(f"  赚钱效应: {up_ratio:.1f}%")
print(f"")
print(f"  涨停(≥9.5%): {limit_up} 只")
print(f"  跌停(≤-9.5%): {limit_down} 只")
print(f"")
print(f"  涨幅>3%: {more_3} 只")
print(f"  涨幅>5%: {more_5} 只")
print(f"  跌幅>3%: {less_3} 只")
print(f"  跌幅>5%: {less_5} 只")

# 主要指数行情
print("\n" + "=" * 60)
print("2. 主要指数行情:")
index_map = {
    '000001': '上证指数',
    '399001': '深证成指',
    '399006': '创业板指',
    '000688': '科创50',
}
for code, name in index_map.items():
    row = df[df['代码'] == code]
    if not row.empty:
        price = float(row.iloc[0]['最新价'])
        change = float(row.iloc[0]['涨跌幅'])
        change_str = f"+{change:.2f}%" if change >0 else f"{change:.2f}%"
        print(f"  {name}: {price:.2f}  {change_str}")

# 行业板块领涨领跌
print("\n" + "=" * 60)
print("3. 领涨/领跌个股:")
print("  涨幅前10名:")
df_sorted = df_stock.sort_values('涨跌幅_num', ascending=False)
for i in range(10):
    if i >= len(df_sorted): break
    row = df_sorted.iloc[i]
    print(f"    {row['代码']} {row['名称']}: {row['涨跌幅_num']:.1f}%")

print("\n  跌幅前10名:")
df_sorted_down = df_stock.sort_values('涨跌幅_num', ascending=True)
for i in range(10):
    if i >= len(df_sorted_down): break
    row = df_sorted_down.iloc[i]
    print(f"    {row['代码']} {row['名称']}: {row['涨跌幅_num']:.1f}%")

print("\n" + "=" * 60)
print("数据获取完成")
