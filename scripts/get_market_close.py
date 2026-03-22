#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-03-16 收盘大盘分析
"""

import akshare as ak
import pandas as pd
from datetime import datetime

print("=" * 60)
print("2026年3月16日 收盘大盘分析")
print("获取时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 获取全部行情数据
df = ak.stock_zh_a_spot()
print(f"总计获取 {len(df)} 条行情数据")

# 全市场涨跌统计
print("\n1. 全市场涨跌统计:")
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
print("2. 主要指数收盘行情:")
index_map = {
    '000001': '上证指数',
    '399001': '深证成指',
    '399006': '创业板指',
    '000688': '科创50',
    'sh000001': '上证指数',
    'sz399001': '深证成指',
    'sz399006': '创业板指',
    'sh000688': '科创50',
}
for code, name in index_map.items():
    row = df[df['代码'] == code]
    if not row.empty:
        price = float(row.iloc[0]['最新价'])
        change = float(row.iloc[0]['涨跌幅'])
        change_str = f"+{change:.2f}%" if change >0 else f"{change:.2f}%"
        print(f"  {name}: {price:.2f}  {change_str}")
        break

# 异动板块扫描（扫描所有概念板块）
print("\n" + "=" * 60)
print("3. 异动板块扫描（涨幅前10名）:")
# 常见热门板块个股列表
hot_sectors = {
    'AI算力': ['sh688041', 'sz300474', 'sh688256', 'sz000977', 'sz300223', 'sz300458'],
    '半导体': ['sh600171', 'sz002180', 'sz300661', 'sz002049', 'sz002916', 'sh688295'],
    '光伏': ['sh600438', 'sz002459', 'sz300274', 'sz300763', 'sh601012', 'sh688390'],
    '储能': ['sz300750', 'sz300014', 'sz002594', 'sz002709', 'sz002812', 'sh688348'],
    '军工': ['sh600879', 'sz002179', 'sz000733', 'sz000768', 'sz300726', 'sh600316'],
    '汽车整车': ['sz002594', 'sh600104', 'sz000625', 'sz000550', 'sh601238', 'sh601633'],
}

sector_results = []
for sector_name, stock_codes in hot_sectors.items():
    up_count = 0
    limit_up_count = 0
    total = len(stock_codes)
    avg_change = 0
    for code in stock_codes:
        row = df[df['代码'] == code]
        if not row.empty:
            change = float(row.iloc[0]['涨跌幅'])
            avg_change += change
            if change > 0:
                up_count +=1
            if change >=9.5:
                limit_up_count +=1
    if total ==0:
        continue
    avg_change = avg_change / total
    up_ratio = up_count / total *100
    sector_results.append({
        'name': sector_name,
        'avg_change': avg_change,
        'up_ratio': up_ratio,
        'limit_up': limit_up_count
    })

# 按平均涨幅排序
sector_results = sorted(sector_results, key=lambda x: x['avg_change'], reverse=True)
for i, sector in enumerate(sector_results[:10]):
    status = "✅ 异动" if sector['avg_change']>2 and sector['limit_up']>=3 and sector['up_ratio']>=70 else ""
    print(f"  {i+1}. {sector['name']}: 平均涨幅 {sector['avg_change']:.2f}%, 上涨占比 {sector['up_ratio']:.1f}%, 涨停 {sector['limit_up']}只 {status}")

print("\n" + "=" * 60)
print("4. 涨停个股前10名:")
df_sorted_up = df.sort_values('涨跌幅_num', ascending=False).head(10)
for _, row in df_sorted_up.iterrows():
    print(f"  {row['代码']} {row['名称']}: {row['涨跌幅_num']:.1f}%")

print("\n" + "=" * 60)
print("分析完成")
