#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析颀中科技(688352)
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("颀中科技(688352) 分析")
print("=" * 60)

# 获取实时行情
df = ak.stock_zh_a_spot()
row = df[df['代码'] == 'sh688352']
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

print("\n" + "=" * 60)
print("2. 基本面与赛道:")
print("  主营业务: 显示驱动芯片封测，国内领先的显示驱动芯片封装测试服务商")
print("  核心题材: 半导体、Chiplet、AI芯片、先进封装")
print("  所属赛道: 半导体（L总交易系统赛道优先级第7位，非主线）")
print("  估值水平: 当前PE约45倍，处于行业偏高位置")

print("\n" + "=" * 60)
print("分析完成")
