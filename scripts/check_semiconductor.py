#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查半导体存储板块异动情况
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("半导体存储板块异动检查")
print("获取时间：", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

# 获取概念板块行情
print("\n1. 概念板块涨幅前20名:")
try:
    # 获取所有概念板块行情
    concept_df = ak.stock_zh_a_spot_concept()
    concept_df['涨跌幅'] = pd.to_numeric(concept_df['涨跌幅'], errors='coerce')
    # 按涨跌幅排序
    concept_df = concept_df.sort_values('涨跌幅', ascending=False)
    top20 = concept_df.head(20)
    
    # 打印前20
    for _, row in top20.iterrows():
        print(f"  {row['板块']}: {row['涨跌幅']:.2f}%  涨跌: {row['上涨']}/{row['下跌']}")
    
    # 筛选半导体/存储相关板块
    print("\n" + "=" * 60)
    print("2. 半导体/存储相关板块情况:")
    semis = concept_df[concept_df['板块'].str.contains('半导体|存储|芯片|集成电路|封测|先进封装', case=False)]
    if not semis.empty:
        for _, row in semis.iterrows():
            print(f"  {row['板块']}: {row['涨跌幅']:.2f}%  涨跌: {row['上涨']}/{row['下跌']}")
    else:
        print("  未进入前20，无明显异动")

    # 存储相关个股
    print("\n" + "=" * 60)
    print("3. 存储概念龙头股行情:")
    storage_stocks = {
        'sh688047': '龙芯中科',
        'sh603986': '兆易创新',
        'sz000925': '众合科技',
        'sz300661': '圣邦股份',
        'sz300223': '北京君正',
        'sz002405': '四维图新',
        'sz300458': '全志科技',
        'sh603160': '汇顶科技'
    }
    
    df_all = ak.stock_zh_a_spot()
    up_count = 0
    for code, name in storage_stocks.items():
        row = df_all[df_all['代码'] == code]
        if not row.empty:
            change = float(row.iloc[0]['涨跌幅'])
            if change > 0:
                up_count += 1
            print(f"  {name}({code}): {row.iloc[0]['最新价']}  {change:.2f}%")
    
    print(f"\n  存储龙头上涨家数: {up_count}/{len(storage_stocks)}")
    
except Exception as e:
    print(f"获取数据失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("检查完成")
