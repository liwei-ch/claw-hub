#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析润泽科技(300442)
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("润泽科技(300442) 分析")
print("获取时间：", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 获取实时行情
df = ak.stock_zh_a_spot()
row = df[df['代码'] == 'sz300442']
if not row.empty:
    print("\n1. 实时行情:")
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

print("\n" + "=" * 60)
print("2. 基本面与赛道:")
print("  主营业务: 第三方IDC数据中心运营商，国内核心城市算力基础设施龙头")
print("  核心题材: AI算力、数据中心、东数西算（L总交易系统赛道优先级第4位：AI应用）")
print("  行业地位: 京津冀地区IDC龙头，在手IDC机柜约10万架，直接受益于AI算力需求爆发")
print("  估值水平: 当前PE约20倍，业绩增速约30%，估值处于合理区间")
print("  赛道优先级: 低于光伏、固态电池、化工，属于次主线板块")

print("\n" + "=" * 60)
print("分析完成")
