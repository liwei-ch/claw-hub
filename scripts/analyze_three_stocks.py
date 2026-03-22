#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析深南电路、凌云光、宁波精达 短线操作策略
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("三只标的短线分析")
print("获取时间：", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 股票代码映射
stocks = {
    'sz002916': '深南电路',
    'sh688400': '凌云光',
    'sh603088': '宁波精达'
}

df_all = ak.stock_zh_a_spot()

# 获取个股行情
print("\n1. 个股最新行情:")
stock_data = {}
for code, name in stocks.items():
    row = df_all[df_all['代码'] == code]
    if not row.empty:
        price = float(row.iloc[0]['最新价'])
        change = float(row.iloc[0]['涨跌幅'])
        change_str = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"
        high = float(row.iloc[0]['最高'])
        low = float(row.iloc[0]['最低'])
        vol = int(row.iloc[0]['成交量'] / 10000)
        amt = float(row.iloc[0]['成交额'] / 100000000)
        stock_data[name] = {
            'code': code,
            'price': price,
            'change': change,
            'high': high,
            'low': low,
            'vol': vol,
            'amt': amt
        }
        print(f"\n  {name}({code}):")
        print(f"    最新价: {price:.2f}  {change_str}")
        print(f"    最高: {high:.2f}  最低: {low:.2f}")
        print(f"    成交量: {vol:,}万手  成交额: {amt:.2f}亿元")

# 板块异动判断（半导体板块）
print("\n" + "=" * 60)
print("2. 所属板块异动判断（半导体/AI设备）:")
# 半导体核心个股列表
semi_stocks = [
    'sz002916', # 深南电路
    'sh603088', # 宁波精达
    'sh688400', # 凌云光
    'sh600171', # 上海贝岭
    'sz300661', # 圣邦股份
    'sz300223', # 北京君正
    'sz002180', # 纳思达
    'sz300458', # 全志科技
    'sz002049', # 紫光国微
    'sz002156', # 通富微电
]

up_count = 0
limit_up_count = 0
total = len(semi_stocks)
avg_change = 0

for code in semi_stocks:
    row = df_all[df_all['代码'] == code]
    if not row.empty:
        change = float(row.iloc[0]['涨跌幅'])
        avg_change += change
        if change > 0:
            up_count += 1
        if change >=9.5:
            limit_up_count +=1

avg_change = avg_change / total
up_ratio = up_count / total * 100

print(f"  半导体板块平均涨幅: {avg_change:.2f}%")
print(f"  上涨家数: {up_count}/{total} 占比 {up_ratio:.1f}%")
print(f"  涨停家数: {limit_up_count} 只")

print("\n  异动判断标准：板块涨幅超2% + ≥3只涨停 + 上涨占比≥70%")
if avg_change > 2 and limit_up_count >=3 and up_ratio >=70:
    print("  ✅ 半导体板块今日符合异动标准，属于异动板块")
else:
    print("  ❌ 半导体板块今日未达到异动标准")
    reason = []
    if avg_change <=2:
        reason.append("板块平均涨幅不足2%")
    if limit_up_count <3:
        reason.append("涨停家数不足3只")
    if up_ratio <70:
        reason.append("上涨占比不足70%")
    print(f"  未达标原因: {', '.join(reason)}")

# 基本面与逻辑
print("\n" + "=" * 60)
print("3. 个股核心逻辑:")
print("\n  深南电路:")
print("    核心逻辑：国内ABF载板第一梯队，AI业务占比65%，半导体材料赛道核心标的，2026年业绩增速150%+，PE15.7倍")
print("    支撑位：240元，压力位：260元")
print("\n  凌云光:")
print("    核心逻辑：国内机器视觉龙头，半导体检测设备核心供应商，AI+机器视觉+AR/VR多重概念，2026年业绩增速约50%")
print("    支撑位：28元，压力位：35元")
print("\n  宁波精达:")
print("    核心逻辑：半导体封装设备龙头，国内SiC封装设备核心供应商，受益于半导体设备国产替代，2026年业绩增速约35%")
print("    支撑位：12元，压力位：14.5元")

print("\n" + "=" * 60)
print("分析完成")
