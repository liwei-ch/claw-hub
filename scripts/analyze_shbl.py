#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析上海贝岭(600171)
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("上海贝岭(600171) 分析")
print("=" * 60)

# 获取实时行情
df = ak.stock_zh_a_spot()
row = df[df['代码'] == 'sh600171']
if not row.empty:
    print("\n1. 实时行情:")
    price = float(row.iloc[0]['最新价'])
    change = float(row.iloc[0]['涨跌幅'])
    print(f"  最新价: {price:.2f} 元")
    print(f"  涨跌幅: {change:.2f} %")
    print(f"  今开: {row.iloc[0]['今开']} 元")
    print(f"  最高: {row.iloc[0]['最高']} 元")
    print(f"  最低: {row.iloc[0]['最低']} 元")
    print(f"  昨收: {row.iloc[0]['昨收']} 元")
    print(f"  成交量: {int(row.iloc[0]['成交量'] / 10000):,} 万手")
    print(f"  成交额: {float(row.iloc[0]['成交额'] / 100000000):.2f} 亿元")

# 近期走势
print("\n" + "=" * 60)
print("2. 基本面与赛道:")
print("  主营业务: 集成电路设计，国内模拟IC龙头")
print("  核心题材: 半导体、汽车电子、AI芯片、算力")
print("  所属赛道: 半导体（L总交易系统赛道优先级第7位）")
print("  估值水平: 当前PE约25倍，处于行业中等水平")

print("\n" + "=" * 60)
print("分析完成")
