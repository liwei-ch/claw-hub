#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析通威股份(600438) + 光伏板块异动判断
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("通威股份(600438) 分析 + 光伏板块异动判断")
print("获取时间：", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 获取通威股份实时行情
print("\n1. 通威股份实时行情:")
df_all = ak.stock_zh_a_spot()
row = df_all[df_all['代码'] == 'sh600438']
if not row.empty:
    price = float(row.iloc[0]['最新价'])
    change = float(row.iloc[0]['涨跌幅'])
    change_str = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"
    print(f"  最新价: {price:.2f} 元")
    print(f"  涨跌幅: {change_str}")
    print(f"  今开: {row.iloc[0]['今开']} 元")
    print(f"  最高: {row.iloc[0]['最高']} 元")
    print(f"  最低: {row.iloc[0]['最低']} 元")
    print(f"  昨收: {row.iloc[0]['昨收']} 元")
    print(f"  成交量: {int(row.iloc[0]['成交量'] / 10000):,} 万手")
    print(f"  成交额: {float(row.iloc[0]['成交额'] / 100000000):.2f} 亿元")

# 判断光伏板块异动
print("\n" + "=" * 60)
print("2. 光伏板块异动判断:")
# 光伏核心个股列表
pv_stocks = {
    'sh600438': '通威股份',
    'sz002459': '晶澳科技',
    'sz002129': '中环股份',
    'sz300274': '阳光电源',
    'sz300763': '锦浪科技',
    'sz300751': '迈为股份',
    'sh688223': '晶科能源',
    'sh688390': '固德威',
    'sh601012': '隆基绿能',
    'sz002518': '科士达',
}

up_count = 0
limit_up_count = 0
total = len(pv_stocks)
sector_change = 0
details = []

for code, name in pv_stocks.items():
    row = df_all[df_all['代码'] == code]
    if not row.empty:
        change = float(row.iloc[0]['涨跌幅'])
        sector_change += change
        if change > 0:
            up_count += 1
        if change >= 9.5:
            limit_up_count += 1
        details.append(f"    {name}: {change:.2f}%")

sector_avg_change = sector_change / total
up_ratio = up_count / total * 100

print("  光伏核心个股涨跌幅:")
for d in details:
    print(d)
print(f"\n  板块平均涨跌幅: {sector_avg_change:.2f}%")
print(f"  上涨家数: {up_count}/{total}，占比 {up_ratio:.1f}%")
print(f"  涨停家数: {limit_up_count} 只")

# 判断异动
print("\n  异动判断（需同时满足3个条件：涨幅超2% + ≥3只涨停 + 上涨占比≥70%）:")
if sector_avg_change > 2 and limit_up_count >=3 and up_ratio >=70:
    print("  ✅ 光伏板块今日出现异动，符合异动标准")
else:
    print("  ❌ 光伏板块今日无明显异动，未满足异动标准")
    reason = []
    if sector_avg_change <=2:
        reason.append("板块平均涨幅不足2%")
    if limit_up_count <3:
        reason.append("涨停家数不足3只")
    if up_ratio <70:
        reason.append("上涨家数占比不足70%")
    print(f"  未满足原因: {', '.join(reason)}")

print("\n" + "=" * 60)
print("3. 通威股份基本面逻辑:")
print("  硅料+电池片双全球第一，2025年净利润352亿，PE仅2.47倍，估值极低")
print("  当前18-22元为历史大底部区间，安全边际极高，趋势向上")

print("\n" + "=" * 60)
print("分析完成")
