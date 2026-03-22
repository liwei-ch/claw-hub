#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析固德威(688390)
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("固德威(688390) 走势分析")
print("获取时间：", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 获取实时行情
df = ak.stock_zh_a_spot()
row = df[df['代码'] == 'sh688390']
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

# 基本面与赛道
print("\n" + "=" * 60)
print("2. 基本面与赛道:")
print("  主营业务: 光伏组串式逆变器龙头，全球储能逆变器核心供应商")
print("  核心题材: 光伏、储能、新能源（L总交易系统赛道优先级第1位，最高优先级）")
print("  行业地位: 组串式逆变器全球市占率前三，储能逆变器业务增速超100%")
print("  估值水平: 当前PE约22倍，处于历史低位，业绩增速约50%，PEG<0.5，估值优势明显")
print("  逻辑支撑: 全球光伏装机量持续增长，储能需求爆发，逆变器量价齐升")

print("\n" + "=" * 60)
print("分析完成")
