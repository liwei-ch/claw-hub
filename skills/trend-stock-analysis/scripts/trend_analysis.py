#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
趋势票分析工具 - 三级趋势分析（月线→周线→日线）
严格遵循L总的A股交易体系
支持数据双源校验：Tushare + akshare
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 全局配置
MA_PARAMS = [5, 10, 20, 60]  # 均线参数


def format_stock_code(code):
    """格式化股票代码"""
    code = str(code).strip()
    if '.' in code:
        return code
    if code.startswith('6'):
        return f"{code}.SH"
    else:
        return f"{code}.SZ"


def get_stock_name_tushare(pro, ts_code):
    """从Tushare获取股票名称"""
    try:
        df = pro.stock_basic(ts_code=ts_code, fields='ts_code,name,industry')
        if not df.empty:
            return df.iloc[0]['name'], df.iloc[0]['industry']
        return None, None
    except Exception as e:
        print(f"Tushare获取股票基本信息失败: {e}")
        return None, None


def get_kline_tushare(pro, ts_code, freq='D'):
    """从Tushare获取K线数据"""
    try:
        # 根据周期设置开始时间
        if freq == 'M':  # 月线
            start_date = (datetime.now() - timedelta(days=365*5)).strftime('%Y%m%d')
        elif freq == 'W':  # 周线
            start_date = (datetime.now() - timedelta(days=365*2)).strftime('%Y%m%d')
        else:  # 日线
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        
        end_date = datetime.now().strftime('%Y%m%d')
        
        if freq == 'D':
            df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        elif freq == 'W':
            df = pro.weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
        elif freq == 'M':
            df = pro.monthly(ts_code=ts_code, start_date=start_date, end_date=end_date)
        else:
            print(f"不支持的周期: {freq}")
            return None
        
        if df is not None and not df.empty:
            # 按日期升序排列
            df = df.sort_values('trade_date').reset_index(drop=True)
            return df
        return None
    except Exception as e:
        print(f"Tushare获取{freq}K线失败: {e}")
        return None


def get_kline_akshare(code, freq='daily'):
    """从akshare获取K线数据"""
    try:
        import akshare as ak
        
        # 转换代码格式
        code_ak = code.replace('.SZ', '').replace('.SH', '')
        
        # 获取日线数据
        if freq == 'daily':
            df = ak.stock_zh_a_hist(symbol=code_ak, period="daily", start_date="20180101", adjust="qfq")
        elif freq == 'weekly':
            df = ak.stock_zh_a_hist(symbol=code_ak, period="weekly", start_date="20180101", adjust="qfq")
        elif freq == 'monthly':
            df = ak.stock_zh_a_hist(symbol=code_ak, period="monthly", start_date="20180101", adjust="qfq")
        else:
            print(f"不支持的周期: {freq}")
            return None
        
        if df is not None and not df.empty:
            # 统一列名
            column_mapping = {
                '日期': 'trade_date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'vol',
                '成交额': 'amount'
            }
            df = df.rename(columns=column_mapping)
            # 格式化日期
            df['trade_date'] = df['trade_date'].astype(str).str.replace('-', '')
            return df.sort_values('trade_date').reset_index(drop=True)
        return None
    except Exception as e:
        print(f"akshare获取{freq}K线失败: {e}")
        return None


def get_stock_info_akshare(code):
    """从akshare获取股票基本信息"""
    try:
        import akshare as ak
        code_ak = code.replace('.SZ', '').replace('.SH', '')
        # 补零到6位，保持字符串格式
        code_ak = code_ak.zfill(6)
        df = ak.stock_info_a_code_name()
        # code列是字符串，直接比较
        row = df[df['code'] == code_ak]
        if not row.empty:
            return row.iloc[0]['name'], None
        # 尝试另一种方式，如果没找到，直接返回代码当名称
        return f"股票{code_ak}", None
    except Exception as e:
        print(f"akshare获取股票名称失败: {e}")
        code_ak = code.replace('.SZ', '').replace('.SH', '')
        return f"股票{code_ak.zfill(6)}", None


def calculate_ma(df, ma_params=MA_PARAMS):
    """计算均线"""
    df_result = df.copy()
    for ma in ma_params:
        df_result[f'ma{ma}'] = df_result['close'].rolling(window=ma).mean()
    return df_result


def analyze_trend(df):
    """分析趋势
    返回：趋势类型（up/down/sideways）、分析描述
    """
    if len(df) < 60:
        return 'insufficient', '数据不足，无法分析'
    
    # 获取最新数据
    latest = df.iloc[-1]
    
    # 检查均线排列
    ma5 = latest.get('ma5', latest.get('MA5'))
    ma10 = latest.get('ma10', latest.get('MA10'))
    ma20 = latest.get('ma20', latest.get('MA20'))
    ma60 = latest.get('ma60', latest.get('MA60'))
    
    if any(pd.isna(x) for x in [ma5, ma10, ma20, ma60]):
        return 'insufficient', '均线数据不完整'
    
    # 判断均线排列
    is_bullish = ma5 > ma10 > ma20 > ma60
    is_bearish = ma5 < ma10 < ma20 < ma60
    
    # 检查高点和低点
    recent_20 = df.tail(20)
    recent_high = recent_20['high'].max()
    recent_low = recent_20['low'].min()
    prev_20 = df.iloc[-40:-20]
    prev_high = prev_20['high'].max() if len(prev_20) > 0 else 0
    prev_low = prev_20['low'].min() if len(prev_20) > 0 else 0
    
    higher_high = recent_high > prev_high if prev_high > 0 else False
    higher_low = recent_low > prev_low if prev_low > 0 else False
    
    lower_low = recent_low < prev_low if prev_low > 0 else False
    lower_high = recent_high < prev_high if prev_high > 0 else False
    
    # 综合判断
    if is_bullish and higher_high and higher_low:
        return 'up', f'上升趋势：均线多头排列({ma5:.2f}>{ma10:.2f}>{ma20:.2f}>{ma60:.2f})，高点抬升，低点抬高'
    elif is_bearish and lower_low and lower_high:
        return 'down', f'下降趋势：均线空头排列({ma5:.2f}<{ma10:.2f}<{ma20:.2f}<{ma60:.2f})，高点降低，低点创新低'
    else:
        # 判断震荡区间
        max_price = df.tail(40)['high'].max()
        min_price = df.tail(40)['low'].min()
        range_pct = (max_price - min_price) / min_price * 100
        return 'sideways', f'震荡趋势：均线交织，股价在{range_pct:.1f}%区间内波动'


def verify_data(tu_df, ak_df):
    """双源校验数据一致性"""
    if tu_df is None or ak_df is None:
        return False, "至少一个数据源无数据"
    
    # 比较最新收盘价
    tu_close = tu_df.iloc[-1]['close']
    ak_close = ak_df.iloc[-1]['close']
    
    # 计算差异百分比
    diff_pct = abs(tu_close - ak_close) / ((tu_close + ak_close) / 2) * 100
    
    if diff_pct < 2:
        return True, f"数据校验通过，收盘价差异{diff_pct:.2f}%"
    else:
        return False, f"数据校验不通过，收盘价差异{diff_pct:.2f}%超过2%"


def get_combined_data(tu_df, ak_df):
    """获取合并后的数据，如果双源校验通过优先用Tushare，否则用akshare"""
    if tu_df is not None:
        verified, msg = verify_data(tu_df, ak_df)
        print(msg)
        if verified:
            return calculate_ma(tu_df)
    
    if ak_df is not None:
        return calculate_ma(ak_df)
    
    return None


def get_trend_emoji(trend):
    """获取趋势emoji"""
    if trend == 'up':
        return '📈'
    elif trend == 'down':
        return '📉'
    elif trend == 'sideways':
        return '↔️'
    else:
        return '❓'


def get_trend_name(trend):
    """获取趋势名称"""
    name_map = {
        'up': '上升趋势',
        'down': '下降趋势',
        'sideways': '震荡趋势',
        'insufficient': '数据不足'
    }
    return name_map.get(trend, '未知')


def generate_recommendation(monthly_trend, weekly_trend, daily_trend):
    """根据三级趋势组合生成买卖建议"""
    # 定义权重：月线 > 周线 > 日线
    # 下降趋势一票否决
    if monthly_trend == 'down':
        return {
            'action': 'sell',
            'suggestion': '坚决不买',
            'position': '0成仓',
            'reason': '月线下降趋势，长期向下，规避风险'
        }
    
    if weekly_trend == 'down' and monthly_trend != 'up':
        return {
            'action': 'avoid',
            'suggestion': '观望',
            'position': '0成仓',
            'reason': '周线下降趋势，中期向下，等待趋势反转'
        }
    
    # 月线上涨的情况
    if monthly_trend == 'up':
        if weekly_trend == 'up':
            if daily_trend == 'up':
                return {
                    'action': 'buy',
                    'suggestion': '买入/持有',
                    'position': '1-2成仓',
                    'reason': '月线、周线、日线全部多头排列，趋势明确向上，回踩均线加仓'
                }
            elif daily_trend == 'sideways':
                return {
                    'action': 'hold',
                    'suggestion': '持有观望',
                    'position': '现有仓位持有，不加仓',
                    'reason': '月周线向上，日线震荡整理，等待方向选择'
                }
            else:  # daily down
                return {
                    'action': 'hold',
                    'suggestion': '持有等待回调结束',
                    'position': '现有仓位持有，不新开仓',
                    'reason': '月周线向上，日线回调，是良性调整，等待回调企稳后加仓'
                }
        elif weekly_trend == 'sideways':
            if daily_trend == 'up':
                return {
                    'action': 'light_buy',
                    'suggestion': '轻仓试错',
                    'position': '0.5成仓',
                    'reason': '月线向上，周线震荡，日线向上突破，轻仓试探，突破确认加仓'
                }
            else:
                return {
                    'action': 'wait',
                    'suggestion': '观望等待',
                    'position': '0成仓',
                    'reason': '月线向上，周线震荡日线向下，等待日线企稳'
                }
        else:  # weekly down
            return {
                'action': 'avoid',
                'suggestion': '观望',
                'position': '0成仓',
                'reason': '月线向上但周线向下，中期调整，等待周线企稳'
            }
    
    # 月线震荡
    if monthly_trend == 'sideways':
        if weekly_trend == 'up':
            if daily_trend == 'up':
                return {
                    'action': 'light_buy',
                    'suggestion': '轻仓试错',
                    'position': '0.5-1成仓',
                    'reason': '月线震荡，周线日线向上，轻仓参与，突破区间加仓'
                }
            else:
                return {
                    'action': 'wait',
                    'suggestion': '观望',
                    'position': '0成仓',
                    'reason': '月线震荡，日线向下，等待企稳信号'
                }
        else:
            return {
                'action': 'wait',
                'suggestion': '观望',
                'position': '0成仓',
                'reason': '月线震荡，周线非上涨趋势，等待明确趋势'
            }
    
    # 默认情况
    return {
        'action': 'wait',
        'suggestion': '观望',
        'position': '0成仓',
        'reason': '趋势不明确，等待更好的入场点'
    }


def get_action_color(action):
    """获取操作emoji"""
    color_map = {
        'buy': '🟢',
        'light_buy': '🟡',
        'hold': '🔵',
        'sell': '🔴',
        'avoid': '⚫',
        'wait': '⚪'
    }
    return color_map.get(action, '❓')


def generate_report(stock_name, industry, monthly_trend, monthly_desc, 
                   weekly_trend, weekly_desc, daily_trend, daily_desc, 
                   recommendation):
    """生成markdown分析报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""# 趋势票分析报告

## 基本信息
- **股票名称**: {stock_name}
- **所属行业**: {industry if industry else '未知'}
- **分析日期**: {today}

---

## 三级趋势分析

### 1. 月线分析（长期趋势）
**趋势**: {get_trend_emoji(monthly_trend)} {get_trend_name(monthly_trend)}
**描述**: {monthly_desc}

### 2. 周线分析（中期趋势）
**趋势**: {get_trend_emoji(weekly_trend)} {get_trend_name(weekly_trend)}
**描述**: {weekly_desc}

### 3. 日线分析（短期趋势）
**趋势**: {get_trend_emoji(daily_trend)} {get_trend_name(daily_trend)}
**描述**: {daily_desc}

---

## 综合判断
{get_action_color(recommendation['action'])} **操作建议**: {recommendation['suggestion']}
- **仓位建议**: {recommendation['position']}
- **决策依据**: {recommendation['reason']}

---

## ⚠️ 风险提示
1. 本分析基于公开数据和技术分析，不构成投资建议
2. 市场有风险，投资需谨慎
3. 严格按照交易体系执行，做好止损计划（单票最大回撤不超过15%）
"""
    return report


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python trend_analysis.py <股票代码>")
        print("示例: python trend_analysis.py 000001")
        print("示例: python trend_analysis.py 000001.SZ")
        sys.exit(1)
    
    input_code = sys.argv[1]
    ts_code = format_stock_code(input_code)
    print(f"开始分析股票: {ts_code}")
    
    # 初始化Tushare
    pro = None
    token = os.getenv('TUSHARE_TOKEN')
    if token:
        try:
            import tushare as ts
            pro = ts.pro_api(token)
            print("Tushare初始化成功")
        except Exception as e:
            print(f"Tushare初始化失败: {e}")
    else:
        print("未设置TUSHARE_TOKEN，将仅使用akshare数据源")
    
    # 获取股票基本信息
    stock_name = None
    industry = None
    
    if pro:
        stock_name, industry = get_stock_name_tushare(pro, ts_code)
    
    if stock_name is None:
        stock_name, industry = get_stock_info_akshare(ts_code)
    
    if stock_name is None:
        print("无法获取股票基本信息，请检查代码是否正确")
        sys.exit(1)
    
    print(f"股票名称: {stock_name}")
    
    # 获取月线数据
    print("\n=== 获取月线数据 ===")
    tu_monthly = None
    if pro:
        tu_monthly = get_kline_tushare(pro, ts_code, 'M')
    ak_monthly = get_kline_akshare(ts_code, 'monthly')
    monthly_df = get_combined_data(tu_monthly, ak_monthly)
    if monthly_df is None:
        print("获取月线数据失败")
        sys.exit(1)
    monthly_trend, monthly_desc = analyze_trend(monthly_df)
    print(f"月线趋势: {get_trend_name(monthly_trend)} - {monthly_desc}")
    
    # 获取周线数据
    print("\n=== 获取周线数据 ===")
    tu_weekly = None
    if pro:
        tu_weekly = get_kline_tushare(pro, ts_code, 'W')
    ak_weekly = get_kline_akshare(ts_code, 'weekly')
    weekly_df = get_combined_data(tu_weekly, ak_weekly)
    if weekly_df is None:
        print("获取周线数据失败")
        sys.exit(1)
    weekly_trend, weekly_desc = analyze_trend(weekly_df)
    print(f"周线趋势: {get_trend_name(weekly_trend)} - {weekly_desc}")
    
    # 获取日线数据
    print("\n=== 获取日线数据 ===")
    tu_daily = None
    if pro:
        tu_daily = get_kline_tushare(pro, ts_code, 'D')
    ak_daily = get_kline_akshare(ts_code, 'daily')
    daily_df = get_combined_data(tu_daily, ak_daily)
    if daily_df is None:
        print("获取日线数据失败")
        sys.exit(1)
    daily_trend, daily_desc = analyze_trend(daily_df)
    print(f"日线趋势: {get_trend_name(daily_trend)} - {daily_desc}")
    
    # 生成建议
    recommendation = generate_recommendation(monthly_trend, weekly_trend, daily_trend)
    
    # 生成报告
    report = generate_report(stock_name, industry, 
                           monthly_trend, monthly_desc,
                           weekly_trend, weekly_desc,
                           daily_trend, daily_desc,
                           recommendation)
    
    # 保存报告
    output_dir = os.path.expanduser("~/.openclaw/workspace/trend_analysis_reports")
    os.makedirs(output_dir, exist_ok=True)
    today_str = datetime.now().strftime('%Y%m%d')
    output_file = f"{output_dir}/{ts_code.replace('.', '_')}_{today_str}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + "="*50)
    print(f"分析报告已生成: {output_file}")
    print("="*50 + "\n")
    print(report)


if __name__ == "__main__":
    main()
