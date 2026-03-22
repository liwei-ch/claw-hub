#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查半导体存储板块异动情况 - v2
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("半导体存储板块异动检查")
print("获取时间：", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 存储/半导体核心个股列表
semi_stocks = {
    # 存储芯片
    'sh603986': '兆易创新',
    'sz300223': '北京君正',
    'sz300458': '全志科技',
    'sz002916': '深南电路',
    'sh688256': '寒武纪',
    'sh688041': '海光信息',
    'sz002049': '紫光国微',
    'sh600171': '上海贝岭',
    'sh688352': '颀中科技',
    # AI芯片
    'sz300474': '景嘉微',
    'sh688295': '中复神鹰',
    'sz002371': '北方华创',
    'sz002156': '通富微电',
    'sz002180': '纳思达',
    'sz300053': '欧比特'
}

df_all = ak.stock_zh_a_spot()

up_count = 0
up_3_count = 0
total = len(semi_stocks)
details = []

print("\n半导体/存储核心个股行情:")
for code, name in semi_stocks.items():
    row = df_all[df_all['代码'] == code]
    if not row.empty:
        price = float(row.iloc[0]['最新价'])
        change = float(row.iloc[0]['涨跌幅'])
        if change > 0:
            up_count += 1
        if change > 3:
            up_3_count += 1
        details.append({
            'name': name,
            'code': code,
            'price': price,
            'change': change
        })
        change_str = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"
        print(f"  {name}: {price:.2f}  {change_str}")

print("\n" + "=" * 60)
print("异动分析:")
print(f"  统计个股数量: {total} 只")
print(f"  上涨家数: {up_count} 只，占比 {up_count/total*100:.1f}%")
print(f"  涨幅超3%家数: {up_3_count} 只，占比 {up_3_count/total*100:.1f}%")

if up_count / total > 0.7 and up_3_count >= 3:
    print("  ⚠️  结论：半导体板块有明显异动迹象，上涨占比超70%，多只个股涨幅超3%")
elif up_count / total > 0.5:
    print("  🟡 结论：半导体板块整体偏强，但无明显大面积异动")
else:
    print("  🔵 结论：半导体板块无明显异动，大部分个股表现平淡")

# 查看板块整体涨幅
print("\n" + "=" * 60)
print("半导体ETF行情:")
etf_codes = {
    'sh512480': '半导体ETF',
    'sh512760': '芯片ETF',
    'sz159995': '芯片ETF',
    'sz159813': '半导体ETF'
}

for code, name in etf_codes.items():
    row = df_all[df_all['代码'] == code]
    if not row.empty:
        change = float(row.iloc[0]['涨跌幅'])
        change_str = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"
        print(f"  {name}: {change_str}")

print("\n" + "=" * 60)
print("检查完成")
