#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析航天电子(600879)
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("航天电子(600879) 分析")
print("获取时间：", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 获取实时行情
df = ak.stock_zh_a_spot()
row = df[df['代码'] == 'sh600879']
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
print("  主营业务: 航天军工电子信息化龙头，国内军工电子核心供应商")
print("  核心题材: 军工、卫星互联网、北斗导航（L总交易系统赛道优先级第8位，最低优先级，非主线）")
print("  行业地位: 航天科技集团旗下核心军工电子平台，配套国内多数航天型号")
print("  估值水平: 当前PE约45倍，业绩增速约15%，估值偏高")
print("  赛道优先级: 低于所有其他板块，属于最末优先级非主线板块，按规则不建议配置")

print("\n" + "=" * 60)
print("分析完成")
