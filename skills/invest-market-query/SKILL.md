---
name: market-query-skill
description: 专业、高准确度的A股市场数据查询工具，支持三大核心功能：1. 大盘情绪查询 2. 大盘走势查询 3. 个股信息查询，所有数据经过双源交叉校验确保准确性。
persona: invest
---

# 市场数据查询Skill (market-query-skill)
## 功能说明
专业、高准确度的A股市场数据查询工具，严格调用官方auto_trade仓库(https://github.com/liwei-ch/auto_trade/tree/master/skills)接口，支持三大核心功能：
1. 大盘情绪查询：返回涨跌家数、涨跌停/炸板数据、北向资金、两融余额、股指期货升贴水、情绪等级等20+核心指标
2. 大盘走势查询：支持上证、深成、创业板、科创50、北证50等核心指数的行情、均线、技术指标查询
3. 个股信息查询：返回个股行情、基本面、技术指标、重大事件、风险提示等全量信息

所有输出数据经过双源交叉校验，偏差≤1%取平均值，>1%触发第三源验证，不一致/异常数据直接拦截，禁止输出，确保数据100%准确可靠。

## 依赖要求
- 已配置git访问权限，可拉取git@github.com:liwei-ch/auto_trade.git仓库
- 底层依赖services.market_service已正确配置数据源接口权限

## 使用方法
### 1. 大盘情绪查询
```python
from market_query_skill import market_query_skill
result = market_query_skill.query_market_emotion(date="2026-03-17")
```
#### 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 否 | 查询日期，格式YYYY-MM-DD，默认当前交易日 |

#### 返回示例
```json
{
  "success": true,
  "data": {
    "date": "2026-03-17",
    "up_count": 2856,
    "down_count": 1923,
    "flat_count": 212,
    "up_down_ratio": 1.49,
    "limit_up_count": 46,
    "limit_down_count": 8,
    "broken_limit_up_count": 12,
    "broken_limit_up_rate": 20.69,
    "northbound_flow": 32.56,
    "margin_balance_change": 12.34,
    "ih_basis": 12.5,
    "if_basis": 8.2,
    "ic_basis": -5.3,
    "im_basis": -12.1,
    "median_gain": 0.32,
    "sector_up_count": 22,
    "sector_down_count": 9,
    "emotion_level": "贪婪",
    "emotion_score": 72
  },
  "message": "大盘情绪查询成功"
}
```

---
### 2. 大盘走势查询
```python
from market_query_skill import market_query_skill
# 查询默认五大核心指数
result = market_query_skill.query_index_trend(date="2026-03-17")
# 自定义查询指数
result = market_query_skill.query_index_trend(index_list=["000001.SH", "399006.SZ"], date="2026-03-17")
```
#### 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| index_list | array[string] | 否 | 指数代码列表，默认查询["000001.SH", "399001.SZ", "399006.SZ", "000688.SH", "899050.BJ"]（上证、深成、创业板、科创50、北证50） |
| date | string | 否 | 查询日期，格式YYYY-MM-DD，默认当前交易日 |

#### 返回示例
```json
{
  "success": true,
  "data": [
    {
      "ts_code": "000001.SH",
      "name": "上证指数",
      "date": "2026-03-17",
      "open": 3056.23,
      "high": 3078.45,
      "low": 3048.12,
      "close": 3072.56,
      "change": 1.23,
      "volume": 235.6,
      "amount": 2897.45,
      "volume_ratio": 1.12,
      "ma5": 3052.34,
      "ma10": 3041.23,
      "ma20": 3032.12,
      "ma60": 3012.45,
      "macd": 12.34,
      "rsi": 62.5,
      "leading_sector": "半导体",
      "leading_sector_change": 4.56,
      "lagging_sector": "煤炭",
      "lagging_sector_change": -2.34,
      "main_flow": 56.78
    }
  ],
  "message": "指数走势查询成功"
}
```

---
### 3. 个股信息查询
```python
from market_query_skill import market_query_skill
result = market_query_skill.query_stock_info(ts_code="600438.SH", date="2026-03-17")
```
#### 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ts_code | string | 是 | 股票代码，格式如600000.SH、000001.SZ |
| date | string | 否 | 查询日期，格式YYYY-MM-DD，默认当前交易日 |

#### 返回示例
```json
{
  "success": true,
  "data": {
    "ts_code": "600438.SH",
    "name": "通威股份",
    "date": "2026-03-17",
    "open": 21.23,
    "high": 21.78,
    "low": 21.05,
    "close": 21.65,
    "change": 2.34,
    "volume": 123.45,
    "amount": 26.78,
    "volume_ratio": 1.45,
    "turnover_rate": 1.23,
    "pe": 2.47,
    "pb": 1.12,
    "total_market_cap": 1456.78,
    "float_market_cap": 1423.45,
    "ma5": 21.12,
    "ma10": 20.89,
    "ma20": 20.45,
    "ma60": 19.87,
    "northbound_holding_ratio": 8.76,
    "margin_balance": 23.45,
    "latest_announcement": "2025年全年净利润352亿元，同比增长12.3%",
    "is_dragon_tiger": false,
    "dragon_tiger_net_buy": 0,
    "risk_warning": "无"
  },
  "message": "个股信息查询成功"
}
```

## 错误码说明
| 错误码 | 说明 |
|------|------|
| 400 | 参数错误/查询失败（如股票代码不存在、非交易日等） |
| 500 | 服务器异常/数据源异常 |

## 强制规则（硬编码实现）
1. 涨跌停阈值：主板≥9%、科创板/创业板≥18%、北交所≥27%
2. 板块异动判断：平均涨幅≥2% + 涨停≥3只 + 上涨占比≥70%
3. 放量/缩量判断：量比≥1.5=放量，量比≤0.7=缩量，0.7<量比<1.5=平量
4. 数据单位：金额统一为亿元、百分比保留2位小数、数量为整数