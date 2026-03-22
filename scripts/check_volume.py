#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比近几日成交量，判断是放量还是缩量
"""

import akshare as ak
import pandas as pd

print("=" * 60)
print("近5日成交量对比")
print("获取时间：", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

stocks = {
    'sz300442': '润泽科技',
    'sz002050': '三花智控',
    'sh600879': '航天电子'
}

for code, name in stocks.items():
    print(f"\n📌 {name}({code}):")
    try:
        # 获取近5日日K线
        df = ak.stock_zh_a_daily(symbol=code, start_date=(pd.Timestamp.now() - pd.Timedelta(days=10)).strftime("%Y%m%d"), adjust="")
        df = df.sort_values('date', ascending=False).head(5)
        df['成交量(万手)'] = df['volume'] / 10000
        df['成交额(亿元)'] = df['amount'] / 100000000
        print(df[['date', 'close', '涨跌幅', '成交量(万手)', '成交额(亿元)']].to_string(index=False))
        
        avg_vol_4d = df['成交量(万手)'].iloc[1:].mean()
        today_vol = df['成交量(万手)'].iloc[0]
        vol_ratio = today_vol / avg_vol_4d
        
        if vol_ratio >= 1.5:
            vol_type = "放量"
        elif vol_ratio <= 0.7:
            vol_type = "缩量"
        else:
            vol_type = "平量"
        
        print(f"\n  前4日平均成交量: {avg_vol_4d:.1f}万手")
        print(f"  今日成交量: {today_vol:.1f}万手")
        print(f"  量比: {vol_ratio:.2f} → {vol_type}")
        
    except Exception as e:
        print(f"  获取数据失败: {e}")

print("\n" + "=" * 60)
print("分析完成")
