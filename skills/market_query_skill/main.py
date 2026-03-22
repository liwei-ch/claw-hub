import requests
import argparse
import json
from datetime import datetime

# API基础地址，根据用户部署调整
BASE_URL = "https://ivone.me/ar"

def get_sentiment(date=None):
    """查询大盘情绪"""
    params = {}
    if date:
        params['date'] = date
    try:
        response = requests.get(f"{BASE_URL}/api/market/sentiment", params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        print("📊 大盘情绪分析")
        print(f"日期: {data['date']}")
        print(f"上涨家数: {data['rise_count']} | 下跌家数: {data['fall_count']} | 平盘: {data['flat_count']}")
        print(f"涨停: {data['limit_up_count']} | 跌停: {data['limit_down_count']}")
        print(f"北向资金净流入: {data['northbound_flow']:.2f} 亿元")
        print(f"两融余额: {data['margin_balance']:.2f} 亿元")
        print(f"沪深300期指升贴水: {data['index_future_basis']:.2f} 点")
        print(f"赚钱效应: {data['profit_effect']:.2f}%")
        print(f"情绪等级: {data['sentiment_level']}")
    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")

def get_trend(index_list=None, date=None):
    """查询大盘走势"""
    params = {}
    if index_list:
        params['index_list'] = json.dumps(index_list)
    if date:
        params['date'] = date
    try:
        response = requests.get(f"{BASE_URL}/api/market/trend", params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        print("📈 大盘走势分析")
        print(f"日期: {data['date']}")
        print("\n核心指数表现:")
        for idx in data['index_list']:
            color = "✅" if idx['change'] >= 0 else "❌"
            print(f"{color} {idx['name']}: {idx['close']:.2f} | {idx['change']:+.2f}% | 成交量: {idx['volume']:.2f}亿 | 量比: {idx['volume_ratio']:.2f} | 趋势: {idx['trend']}")
        print("\n领涨板块:")
        for sec in data['main_sector']:
            print(f"🚀 {sec['sector_name']}: {sec['change']:+.2f}% | 资金流入: {sec['fund_inflow']:.2f}亿 | 涨停: {sec['limit_up_count']}只")
    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")

def get_stock_info(ts_code, date=None):
    """查询个股信息"""
    params = {'ts_code': ts_code}
    if date:
        params['date'] = date
    try:
        response = requests.get(f"{BASE_URL}/api/stock/info", params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"📋 {data['name']}({data['ts_code']}) 分析")
        print(f"所属行业: {data['industry']}")
        print(f"收盘价: {data['close']:.2f}元 | 涨跌幅: {data['change']:+.2f}% | 成交额: {data['volume']:.2f}亿")
        print(f"动态PE: {data['pe']:.2f} | 市净率: {data['pb']:.2f}")
        print(f"2025年净利润: {data['net_profit_2025']:.2f}亿 | 同比增速: {data['net_profit_yoy']:+.2f}%")
        print(f"5日均线: {data['ma5']:.2f} | 10日均线: {data['ma10']:.2f} | 20日均线: {data['ma20']:.2f}")
        print(f"支撑位: {data['support']:.2f} | 压力位: {data['resistance']:.2f}")
        if data['announcement']:
            print("\n📢 最近公告:")
            for ann in data['announcement']:
                print(f"- {ann['pub_date']}: {ann['title']}")
        if data['dragon_tiger']:
            print("\n🏆 龙虎榜数据:")
            print(f"机构净买入: {data['dragon_tiger']['institution_net']:.2f}亿 | 买入总额: {data['dragon_tiger']['buy_amount']:.2f}亿 | 卖出总额: {data['dragon_tiger']['sell_amount']:.2f}亿")
        print(f"\n北向资金当日变动: {data['northbound_change']:.2f}万股")
        print(f"融资余额当日变动: {data['margin_change']:.2f}亿元")
    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="市场数据查询工具")
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # 大盘情绪子命令
    parser_sentiment = subparsers.add_parser('sentiment', help='查询大盘情绪')
    parser_sentiment.add_argument('date', nargs='?', help='查询日期，格式YYYY-MM-DD')
    
    # 大盘走势子命令
    parser_trend = subparsers.add_parser('trend', help='查询大盘走势')
    parser_trend.add_argument('index_list', nargs='*', help='指数代码列表，默认所有核心指数')
    parser_trend.add_argument('--date', help='查询日期，格式YYYY-MM-DD')
    
    # 个股查询子命令
    parser_stock = subparsers.add_parser('stock', help='查询个股信息')
    parser_stock.add_argument('ts_code', help='股票代码，格式如600438.SH')
    parser_stock.add_argument('date', nargs='?', help='查询日期，格式YYYY-MM-DD')
    
    args = parser.parse_args()
    
    if args.command == 'sentiment':
        get_sentiment(args.date)
    elif args.command == 'trend':
        index_list = args.index_list if args.index_list else None
        get_trend(index_list, args.date)
    elif args.command == 'stock':
        get_stock_info(args.ts_code, args.date)
