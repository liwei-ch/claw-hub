import tushare as ts
import pandas as pd

# 初始化tushare
ts.set_token('e938714f24c7f7904d7e4a18c68a03f189b7d8f3b2c4a6d7f8e9a0b1c2d3e4f5')
pro = ts.pro_api()

# 获取最近一周的交易日（2026年3月10日到3月17日）
df = pro.daily_info(start_date='20260310', end_date='20260317', fields='trade_date,up_count,down_count,equal_count')

# 按日期倒序排列
df = df.sort_values('trade_date', ascending=False)

# 格式化输出
print("最近一周A股涨跌家数统计：")
print("="*50)
for _, row in df.iterrows():
    date = f"{row['trade_date'][:4]}-{row['trade_date'][4:6]}-{row['trade_date'][6:]}"
    print(f"📅 {date}")
    print(f"   上涨家数：{int(row['up_count'])} 只")
    print(f"   下跌家数：{int(row['down_count'])} 只")
    print(f"   平盘家数：{int(row['equal_count'])} 只")
    print(f"   涨跌比：{round(row['up_count']/row['down_count'],2) if row['down_count']>0 else '∞'}")
    print("-"*50)
