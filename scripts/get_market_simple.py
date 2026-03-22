#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取今日A股大盘简单行情数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime

print("=" * 60)
print("A股大盘今日行情分析 (2026-03-16)")
print("获取时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 获取全部数据
df = ak.stock_zh_a_spot()
print(f"\n总计获取到 {len(df)} 条行情数据")

# 过滤主要指数
print("\n1. 主要指数行情:")
index_map = {
    '000001': '上证指数',
    '399001': '深证成指', 
    '399006': '创业板指',
    '000688': '科创50',
    '000016': '上证50',
    '000905': '中证500',
}

for code, name in index_map.items():
    row = df[df['代码'] == code]
    if not row.empty:
        price = float(row.iloc[0]['最新价'])
        change = float(row.iloc[0]['涨跌幅'])
        print(f"  {name}({code}): {price:.2f}  涨跌幅: {change:.2f}%")

# 全市场统计
print("\n2. 全市场涨跌统计:")
# 只保留6位代码的个股
df_stock = df[df['代码'].str.len() == 6].copy()
df_stock['涨跌幅'] = pd.to_numeric(df_stock['涨跌幅'], errors='coerce')
df_stock = df_stock.dropna(subset=['涨跌幅'])

up = len(df_stock[df_stock['涨跌幅'] > 0])
down = len(df_stock[df_stock['涨跌幅'] < 0])
flat = len(df_stock[df_stock['涨跌幅'] == 0])
total = up + down + flat

limit_up = len(df_stock[df_stock['涨跌幅'] >= 9.5])
limit_down = len(df_stock[df_stock['涨跌幅'] <= -9.5])

more_3 = len(df_stock[df_stock['涨跌幅'] > 3])
more_5 = len(df_stock[df_stock['涨跌幅'] > 5])
less_3 = len(df_stock[df_stock['涨跌幅'] < -3])
less_5 = len(df_stock[df_stock['涨跌幅'] < -5])

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

# 尝试获取北向资金
print("\n3. 北向资金:")
try:
    # 尝试不同接口
    north_df = ak.stock_hsgt()
    print(f"  接口返回列名: {list(north_df.columns)}")
except Exception as e:
    try:
        north_df = ak.fund_hsgt_north_net_flow()
        if not north_df.empty:
            latest = north_df.iloc[-1]
            print(f"  日期: {latest['date']}, 净流入: {float(latest['value']):.2f} 亿元")
    except Exception as e2:
        print(f"  获取北向资金失败: {e}, {e2}")

print("\n" + "=" * 60)
print("数据获取完成")
