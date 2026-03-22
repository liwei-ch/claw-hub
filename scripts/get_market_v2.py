#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取今日A股大盘详细行情数据 - v2 使用正确AkShare接口
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
    # AkShare正确接口：stock_zh_a_spot 获取实时行情
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
                '最新': float(row.iloc[0]['最新']),
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
    all_stock = all_stock[pd.to_numeric(all_stock['最新'], errors='coerce').notna()]
    all_stock['涨跌幅'] = pd.to_numeric(all_stock['涨跌幅'], errors='coerce')
    
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

# 3. 北向资金
print("\n" + "=" * 60)
print("3. 北向资金:")
try:
    # 正确接口名称
    north_df = ak.stock_hsgt_north_net_flow_in()
    # 获取最新一条
    if not north_df.empty:
        latest = north_df.iloc[-1]
        print(f"日期: {latest['date']}")
        print(f"净流入: {float(latest['value']):.2f} 亿元")
except Exception as e:
    print(f"获取北向资金失败: {e}")

# 4. 行业板块涨幅排名
print("\n" + "=" * 60)
print("4. 行业板块排名（涨幅前5）:")
try:
    # 正确接口获取板块行情
    industry_df = ak.stock_zh_a_spot_industry()
    industry_df['涨跌幅'] = industry_df['涨跌幅'].astype(float)
    industry_top = industry_df.sort_values('涨跌幅', ascending=False).head(5)
    for _, row in industry_top.iterrows():
        print(f"  {row['板块']}: {row['涨跌幅']:.2f}%  涨跌家数: {row['上涨']}/{row['下跌']}")
except Exception as e:
    print(f"获取板块数据失败: {e}")
    import traceback
    traceback.print_exc()

# 5. 概念板块涨幅排名
print("\n" + "=" * 60)
print("5. 概念板块排名（涨幅前5）:")
try:
    concept_df = ak.stock_zh_a_spot_concept()
    concept_df['涨跌幅'] = concept_df['涨跌幅'].astype(float)
    concept_top = concept_df.sort_values('涨跌幅', ascending=False).head(5)
    for _, row in concept_top.iterrows():
        print(f"  {row['板块']}: {row['涨跌幅']:.2f}%  涨跌: {row['上涨']}/{row['下跌']}")
except Exception as e:
    print(f"获取概念板块数据失败: {e}")

print("\n" + "=" * 60)
print("数据获取完成")
