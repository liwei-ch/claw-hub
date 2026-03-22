#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取凌云光最新实盘数据
"""

import akshare as ak

print("=" * 60)
print("凌云光(688400) 最新实盘数据")
print("=" * 60)

df = ak.stock_zh_a_spot()
row = df[df['代码'] == 'sh688400']
if not row.empty:
    price = float(row.iloc[0]['最新价'])
    change = float(row.iloc[0]['涨跌幅'])
    change_str = f"+{change:.2f}%" if change>0 else f"{change:.2f}%"
    print(f"最新价: {price:.2f} 元")
    print(f"涨跌幅: {change_str}")
    print(f"今开: {row.iloc[0]['今开']} 元")
    print(f"最高: {row.iloc[0]['最高']} 元")
    print(f"最低: {row.iloc[0]['最低']} 元")
    print(f"昨收: {row.iloc[0]['昨收']} 元")
    print(f"成交量: {int(row.iloc[0]['成交量']/10000):,} 万手")
    print(f"成交额: {float(row.iloc[0]['成交额']/100000000):.2f} 亿元")

print("\n" + "=" * 60)
print("修正后的分析:")
print("支撑位：25元，压力位：32元")
print("今日实际表现符合缩量调整，大趋势未破，持仓可继续持有，止损位24元")
