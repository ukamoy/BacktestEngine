# encoding: UTF-8
"""
展示如何执行策略回测。
"""
from __future__ import division
import json
from ctaBacktesting import BacktestingEngine
from util.ctaBase import *

if __name__ == '__main__':
    from StrategyBollBand import BollBandsStrategy
    
    # 创建回测引擎
    engine = BacktestingEngine()

    # 设置引擎的回测模式为K线
    engine.setBacktestingMode(engine.BAR_MODE)
    # 设置使用的历史数据库
    engine.setDBConnect('localhost',27017)
    engine.setDatabase('VnTrader_1Min_Db')

    # 设置回测用的数据起始日期，initHours 默认值为 0
    engine.setStartDate('20181206 06:00',initHours = 6000)   
    engine.setEndDate('20181207 08:00')

    # 设置交易标的相关参数
    engine.setCapital(1000000)  # 设置起始资金，默认值是1,000,000
    engine.setSymbolList(['rb:SHF','jm:DCE'])  # 设置交易品种列表
    engine.setSlippage([0.01,0.05])       # 滑点比率
    engine.setRate([0.3/10000,0.00001])   # 手续费率
    engine.setSize([300,500])         # 合约乘数
    engine.setPriceTick([0.2,0.3])    # 最小价格变动
    engine.setAnnualDays(240)         # 设置年交易日
    
    # 策略报告默认不输出，默认文件夹生成于当前文件夹下
    engine.setLog(True,"D:\\backtest_data\\log\\")    # 设置是否输出日志和交割单, 默认值是不输出False
    engine.setCachePath("D:\\backtest_data\\")        # 设置本地数据缓存的路径，默认存在用户文件夹内
    
    # 在引擎中创建策略对象，setting为策略使用的参数
    with open("./CTA_setting.json") as f:
        setting = json.load(f)[0]
    engine.initStrategy(BollBandsStrategy, setting)
    
    # 开始跑回测
    engine.runBacktesting(source = "csv")

    # 显示回测结果
    engine.showBacktestingResult()
    engine.showDailyResult()