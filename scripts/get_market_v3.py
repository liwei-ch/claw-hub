#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取今日A股大盘详细行情数据 - v3 修正列名
"""

import akshare as ak
import pandas as pd
from datetime import datetime

print("=" * 60)
print("A股大盘今日详细行情分析")
print("获取时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 1. 获取主要指数实时行情
print("\n1. 主要指数行情:")
try:
    spot_df = ak.stock_zh_a_spot()
    # 过滤主要指数
    index_codes = ['000001', '399001', '399006', '000688', '000016', '000905']
    index_names = ['上证指数', '深证成指', '创业板指', '科创50', '上证50', '中证500']
    
    major_indices = []
    for code, name in zip(index_codes, index_names):
        row = spot_df[spot_df['代码'] == code]
        if not row.empty:
            major_indices.append({
                '代码': code,
                '名称': name,
                '最新': float(row.iloc[0]['最新价']),
                '涨跌幅': float(row.iloc[0]['涨跌幅'])
            })
    
    if major_indices:
        df = pd.DataFrame(major_indices)
        print(df.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
except Exception as e:
    print(f"获取指数行情失败: {e}")

# 2. 全市场涨跌统计
print("\n" + "=" * 60)
print("2. 全市场涨跌统计:")
try:
    all_stock = ak.stock_zh_a_spot()
    # 过滤出6位代码的个股
    all_stock = all_stock[all_stock['代码'].str.len() == 6]
    all_stock['最新价'] = pd.to_numeric(all_stock['最新价'], errors='coerce')
    all_stock = all_stock[all_stock['最新价'].notna()]
    all_stock['涨跌幅'] = pd.to_numeric(all_stock['涨跌幅'], errors='coerce')
    all_stock = all_stock[all_stock['涨跌幅'].notna()]
    
    up_count = len(all_stock[all_stock['涨跌幅'] > 0])
    down_count = len(all_stock[all_stock['涨跌幅'] < 0])
    flat_count = len(all_stock[all_stock['涨跌幅'] == 0])
    
    # 统计涨幅分布
    more_3 = len(all_stock[all_stock['涨跌幅'] > 3])
    more_5 = len(all_stock[all_stock['涨跌幅'] > 5])
    more_9 = len(all_stock[all_stock['涨跌幅'] >= 9.5])
    less__3 = len(all_stock[all_stock['涨跌幅'] < -3])
    less__5 = len(all_stock[all_stock['涨跌幅'] < -5])
    less__9 = len(all_stock[all_stock['涨跌幅'] <= -9.5])
    
    total = up_count + down_count + flat_count
    if total > 0:
        up_ratio = up_count / total * 100
        print(f"\n上涨家数: {up_count}")
        print(f"下跌家数: {down_count}")
        print(f"平盘家数: {flat_count}")
        print(f"赚钱效应: {up_ratio:.1f}%")
        print(f"\n涨停(≥9.5%): {more_9} 只")
        print(f"跌停(≤-9.5%): {less__9} 只")
        print(f"\n涨幅超过3%: {more_3}只")
        print(f"涨幅超过5%: {more_5}只")
        print(f"跌幅超过3%: {less__3}只")
        print(f"跌幅超过5%: {less__5}只")
    else:
        print("未获取到有效数据")
except Exception as e:
    print(f"获取涨跌统计失败: {e}")
    import traceback
    traceback.print_exc()

# 3. 北向资金 - 试不同接口
print("\n" + "=" * 60)
print("3. 北向资金:")
try:
    # 正确接口：stock_hsgt_north_day
    north_df = ak.stock_hsgt_north_day()
    if not north_df.empty:
        latest = north_df.iloc[-1]
        print(f"日期: {latest['date']}")
        print(f"净流入: {float(latest['value']):.2f} 亿元")
except Exception as e:
    print(f"获取北向资金失败: {e}")

# 4. 尝试获取板块数据 - 用stock_zh_a_board
print("\n" + "=" * 60)
print("4. 概念板块排名（涨幅前5）:")
try:
    board_df = ak.stock_zh_a_board()
    print(f"返回列名: {list(board_df.columns)}")
    if 'increase_rate' in board_df.columns:
        board_df['increase_rate'] = board_df['increase_rate'].astype(float)
        board_top = board_df.sort_values('increase_rate', ascending=False).head(5)
        for _, row in board_top.iterrows():
            print(f"  {row['name']}: {row['increase_rate']:.2f}%")
    elif 'change_rate' in board_df.columns:
        board_df['change_rate'] = board_df['change_rate'].astype(float)
        board_top = board_df.sort_values('change_rate', ascending=False).head(5)
        for _, row in board_top.iterrows():
            print(f"  {row['name']}: {row['change_rate']:.2f}%")
except Exception as e:
    print(f"获取板块数据失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("数据获取完成")
