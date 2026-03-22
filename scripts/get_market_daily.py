#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取今日A股大盘行情和涨跌停数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime

print("=" * 60)
print("A股大盘今日行情获取")
print("获取时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 1. 获取上证指数实时行情
print("\n1. 获取上证指数行情...")
try:
    # 获取大盘指数实时行情
    spot_df = ak.stock_zh_index_spot()
    # 过滤上证指数、深证成指、创业板指
    major_indices = spot_df[spot_df['名称'].isin(['上证指数', '深证成指', '创业板指', '科创50'])]
    print("\n主要指数行情:")
    print(major_indices[['代码', '名称', '最新', '涨跌幅']].to_string(index=False))
except Exception as e:
    print(f"获取指数行情失败: {e}")

# 2. 获取涨跌停数据
print("\n" + "=" * 60)
print("2. 获取涨跌停数据...")
try:
    # 获取今日涨跌停
    limit_up_down = ak.stock_zh_a_limit_up_down(today=datetime.now().strftime("%Y%m%d"))
    print(f"\n涨停数量: {len(limit_up_down[limit_up_down['涨停'] == True])}")
    print(f"跌停数量: {len(limit_up_down[limit_up_down['跌停'] == True])}")
    print("\n涨停前10只股票:")
    limit_up = limit_up_down[limit_up_down['涨停'] == True].head(10)
    print(limit_up[['代码', '名称', '最新价', '涨跌幅']].to_string(index=False))
except Exception as e:
    print(f"获取涨跌停数据失败: {e}")

# 3. 获取赚钱效应统计
print("\n" + "=" * 60)
print("3. 市场涨跌统计...")
try:
    all_stock = ak.stock_zh_a_spot()
    up_count = len(all_stock[all_stock['涨跌幅'] > 0])
    down_count = len(all_stock[all_stock['涨跌幅'] < 0])
    flat_count = len(all_stock[all_stock['涨跌幅'] == 0])
    total = up_count + down_count + flat_count
    up_ratio = up_count / total * 100
    print(f"\n上涨家数: {up_count}")
    print(f"下跌家数: {down_count}")
    print(f"平盘家数: {flat_count}")
    print(f"赚钱效应: {up_ratio:.1f}%")
except Exception as e:
    print(f"获取涨跌统计失败: {e}")

print("\n" + "=" * 60)
print("数据获取完成")
