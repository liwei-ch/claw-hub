#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取2026-03-16午后大盘行情 简化版
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
print(f"总计获取 {len(df)} 条行情数据")

# 统计全市场涨跌
print("\n1. 全市场涨跌统计:")
# 只要能转成数字的都算
df['涨跌幅_num'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
df = df.dropna(subset=['涨跌幅_num'])

up = len(df[df['涨跌幅_num'] > 0])
down = len(df[df['涨跌幅_num'] < 0])
flat = len(df[df['涨跌幅_num'] == 0])
total = len(df)

limit_up = len(df[df['涨跌幅_num'] >= 9.5])
limit_down = len(df[df['涨跌幅_num'] <= -9.5])

more_3 = len(df[df['涨跌幅_num'] > 3])
more_5 = len(df[df['涨跌幅_num'] > 5])
less_3 = len(df[df['涨跌幅_num'] < -3])
less_5 = len(df[df['涨跌幅_num'] < -5])

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
index_codes = ['000001', '399001', '399006', '000688', 'sh000001', 'sz399001', 'sz399006', 'sh000688']
for code in index_codes:
    row = df[df['代码'] == code]
    if not row.empty:
        name = {'000001':'上证指数','sh000001':'上证指数','399001':'深证成指','sz399001':'深证成指','399006':'创业板指','sz399006':'创业板指','000688':'科创50','sh000688':'科创50'}[code]
        price = float(row.iloc[0]['最新价'])
        change = float(row.iloc[0]['涨跌幅'])
        change_str = f"+{change:.2f}%" if change >0 else f"{change:.2f}%"
        print(f"  {name}: {price:.2f}  {change_str}")
        break

print("\n" + "=" * 60)
print("数据获取完成")
