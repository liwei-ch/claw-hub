#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取今日A股大盘行情 - 最终版本
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

# 查看几个样本
print("\n前5条数据样本:")
print(df.head(5))

# 过滤主要指数
print("\n" + "=" * 60)
print("1. 主要指数行情:")

# 直接从全部数据里找，不管代码前缀
index_name_map = {
    '000001': '上证指数',
    '399001': '深证成指', 
    '399006': '创业板指',
    '000688': '科创50',
    '000016': '上证50',
    '000905': '中证500',
    'sh000001': '上证指数',
    'sz399001': '深证成指',
    'sz399006': '创业板指',
    'sh000688': '科创50',
}

found = False
for code, name in index_name_map.items():
    row = df[df['代码'] == code]
    if not row.empty:
        price = float(row.iloc[0]['最新价'])
        change = float(row.iloc[0]['涨跌幅'])
        print(f"  {name}({code}): {price:.2f}  涨跌幅: {change:.2f}%")
        found = True
if not found:
    print("  未找到主要指数")

# 全市场统计 - 正确方式：包含bj/sh/sz前缀，只判断最后6位是数字
print("\n" + "=" * 60)
print("2. 全市场涨跌统计:")

df_stock = df.copy()
# 提取最后6位判断是否是股票代码
def is_stock_code(code):
    # 代码格式: 000001, sh000001, sz000001, bj830000
    last_six = str(code)[-6:]
    return last_six.isdigit() and len(last_six) == 6

df_stock['is_stock'] = df_stock['代码'].apply(is_stock_code)
df_stock = df_stock[df_stock['is_stock'] == True]
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

# 涨停个股列表
print("\n" + "=" * 60)
print("3. 涨停个股列表 (前15只):")
if total > 0 and 'limit_up' in locals() and limit_up > 0:
    limit_up_df = df_stock[df_stock['涨跌幅_num'] >= 9.5].head(15)
    for _, row in limit_up_df.iterrows():
        print(f"  {row['代码']} {row['名称']}: {row['涨跌幅_num']:.1f}%")
else:
    print("  无涨停数据")

# 跌停个股列表
print("\n4. 跌停个股列表 (全部):")
if total > 0 and 'limit_down' in locals() and limit_down > 0:
    limit_down_df = df_stock[df_stock['涨跌幅_num'] <= -9.5]
    for _, row in limit_down_df.iterrows():
        print(f"  {row['代码']} {row['名称']}: {row['涨跌幅_num']:.1f}%")
else:
    print("  无跌停数据")

# 尝试获取北向资金 - 用正确接口
print("\n" + "=" * 60)
print("5. 北向资金:")
try:
    # 正确接口名称是 stock_hsgt_north_cn
    north_df = ak.stock_hsgt_north_cn()
    if not north_df.empty:
        latest = north_df.iloc[-1]
        print(f"  日期: {latest['date']}")
        print(f"  净流入: {float(latest['value']):.2f} 亿元")
except Exception as e:
    print(f"  获取失败: {e}")

print("\n" + "=" * 60)
print("数据获取完成")
