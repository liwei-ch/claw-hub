from typing import Dict, Any, List, Optional
import sys
import os

# 添加auto_trade仓库到Python路径
sys.path.append(os.path.expanduser("~/.openclaw/workspace/skills/auto_trade"))
from skills import skill_manager

class MarketQuerySkill:
    """
    市场数据查询统一Skill
    整合大盘情绪查询、大盘走势查询、个股信息查询三个核心功能
    所有接口严格调用https://github.com/liwei-ch/auto_trade/tree/master/skills官方接口
    完全遵循官方skill_manager调用规范
    """
    def __init__(self):
        # 使用官方skill_manager管理技能实例
        self.skill_manager = skill_manager
    
    def query_market_emotion(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        查询大盘情绪
        :param date: 查询日期，格式YYYY-MM-DD，默认当前交易日
        :return: 情绪数据字典
        """
        params = {}
        if date:
            params["date"] = date
        result = self.skill_manager.execute_skill("market_emotion_query", params)
        return self._format_result(result)
    
    def query_index_trend(self, index_list: Optional[List[str]] = None, date: Optional[str] = None) -> Dict[str, Any]:
        """
        查询大盘/指数走势
        :param index_list: 指数代码列表，默认查询上证/深成/创业板/科创50/北证50
        :param date: 查询日期，格式YYYY-MM-DD，默认当前交易日
        :return: 指数走势数据字典
        """
        params = {}
        if index_list:
            params["index_list"] = ",".join(index_list)
        if date:
            params["date"] = date
        result = self.skill_manager.execute_skill("index_trend_query", params)
        return self._format_result(result)
    
    def query_stock_info(self, ts_code: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        查询个股信息
        :param ts_code: 股票代码，格式如600000.SH、000001.SZ
        :param date: 查询日期，格式YYYY-MM-DD，默认当前交易日
        :return: 个股信息数据字典
        """
        params = {"ts_code": ts_code}
        if date:
            params["date"] = date
        result = self.skill_manager.execute_skill("stock_info_query", params)
        return self._format_result(result)
    
    def _format_result(self, result) -> Dict[str, Any]:
        """
        格式化返回结果，适配官方SkillResult的model_dump()返回
        """
        result_dict = result.model_dump()
        if result_dict.get("success"):
            return {
                "success": True,
                "data": result_dict.get("data"),
                "message": result_dict.get("message")
            }
        else:
            return {
                "success": False,
                "error_code": result_dict.get("error_code"),
                "message": result_dict.get("message")
            }

# 单例实例
market_query_skill = MarketQuerySkill()
