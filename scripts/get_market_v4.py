#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取今日A股大盘简单行情数据 - v4 修复bug
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
print(f"列名: {list(df.columns)}")
print("\n前3行数据:")
print(df.head(3))

# 过滤主要指数
print("\n" + "=" * 60)
print("1. 主要指数行情:")
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
print("\n" + "=" * 60)
print("2. 全市场涨跌统计:")

# 只保留6位代码，排除bj开头的
df_stock = df.copy()
# 筛选出纯数字6位代码（A股）
df_stock = df_stock[df_stock['代码'].str.match(r'^\d{6}$')]
print(f"筛选后A股个股数量: {len(df_stock)}")

# 转换涨跌幅为数值
df_stock['涨跌幅_num'] = pd.to_numeric(df_stock['涨跌幅'], errors='coerce')
df_stock = df_stock.dropna(subset=['涨跌幅_num'])

up = len(df_stock[df_stock['涨跌幅_num'] > 0])
down = len(df_stock[df_stock['涨跌幅_num'] < 0])
flat = len(df_stock[df_stock['涨跌幅_num'] == 0])
total = len(df_stock)

if total > 0:
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
else:
    print("  没有有效数据")

# 尝试获取北向资金
print("\n" + "=" * 60)
print("3. 北向资金:")
try:
    # 查看akshare有什么接口
    import inspect
    members = [m for m in dir(ak) if 'north' in m.lower() or 'hsgt' in m.lower()]
    print(f"  包含north/hsgt的接口: {members}")
except Exception as e:
    print(f"  错误: {e}")

print("\n" + "=" * 60)
print("数据获取完成")
