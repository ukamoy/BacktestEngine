from __future__ import division
from vnpy.trader.vtConstant import *
from vnpy.trader.app.ctaStrategy.ctaTemplate import (CtaTemplate)
from vnpy.trader.vtUtility import BarGenerator,ArrayManager
import os
import talib as ta
import pandas as pd
import numpy as np
from datetime import time,datetime
########################################################################
class BarStrategy(CtaTemplate):
    className = 'BarStrategy'
    author = 'xingetouzi'
    version = '1.1.11'

    # 策略参数
    size = 800
    transactionPrice = {}
    tradable = False
    # 参数列表，保存了参数的名称
    paramList = ['className']

    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'posDict',
               'transactionPrice']

    # 同步列表，保存了需要保存到数据库的变量名称
    syncList = ['posDict','eveningDict',
               'transactionPrice']
    #----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        super(BarStrategy, self).__init__(ctaEngine, setting)
        self.lots = setting['lots']
    #----------------------------------------------------------------------
    def onInit(self):
        self.symbol = self.symbolList[0]

        self.generateBarDict(self.onBar,size = self.size)
        # self.generateBarDict(self.onBar,3,self.on3MinBar,size =self.size)
        # self.generateBarDict(self.onBar,5,self.on5MinBar,size =self.size)
        # self.generateBarDict(self.onBar,30,self.on30MinBar,size =self.size)
        self.generateBarDict(self.onBar,60,self.on60MinBar,size =self.size)
        self.bgDayDict= BarGenerator(self.onCandle,runningTime =(14,59))
        self.bgWeekDict = BarGenerator(self.onWCandle)
        self.bgMonDict = BarGenerator(self.onMCandle)
        self.amweekDict = ArrayManager(25)
        self.ammonDict = ArrayManager(6)
        for s in self.symbolList:
            kline = self.loadHistoryBar(s,'1min', since = '20180410')
            for index, bar in enumerate(kline):
                self.onBar(bar)

    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
    def onStop(self):
        self.putEvent()
    def onRestore(self):
        """恢复策略（必须由用户继承实现）"""
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        self.bgDict[tick.vtSymbol].updateTick(tick)
    # ---------------------------------------------------------------------
    def onBar(self, bar):
        # self.bg3Dict[self.symbol].updateBar(bar)
        # self.bg5Dict[self.symbol].updateBar(bar)
        # self.bg30Dict[self.symbol].updateBar(bar)
        self.bg60Dict[self.symbol].updateBar(bar)
        self.bgDayDict.updateCandle(bar)
        # self.writeCtaLog('onBar: %s '%bar.__dict__)
    #----------------------------------------------------------------------
    # def on3MinBar(self, bar):
    #     # self.writeCtaLog('on----------6666666666666666------------Bar: %s '%bar.datetime)
    #     self.am3Dict[self.symbol].updateBar(bar)
    # def on5MinBar(self, bar):
    #     # self.writeCtaLog('on----------6666666666666666------------Bar: %s '%bar.datetime)
    #     self.am5Dict[self.symbol].updateBar(bar)
    # def on30MinBar(self, bar):
    #     # self.writeCtaLog('on----------6666666666666666------------Bar: %s '%bar.datetime)
    #     self.am30Dict[self.symbol].updateBar(bar)
    def on60MinBar(self, bar):
        # self.writeCtaLog('on----------6666666666666666------------Bar: %s '%bar.datetime)
        self.am60Dict[self.symbol].updateBar(bar)
    #----------------------------------------------------------------------
    def onCandle(self,Candle):
        """Daily Candles"""
        # self.writeCtaLog('on----------dayyyyyyyyyyy------------Bar: %s '%bar.datetime)
        self.bgWeekDict.updateWCandle(Candle)
        self.bgMonDict.updateMCandle(Candle)
    def onWCandle(self,Candle):
        """Week Candles"""
        self.amweekDict.updateBar(Candle)
        # if self.amweekDict.inited:
        #     print(self.amweekDict.DataFrame())
        # self.writeCtaLog('on----------xxxxxxxxxxxxxxxxxxx------------Bar: %s '%Candle.datetime)
    def onMCandle(self,Candle):
        """Month Candles"""
        self.ammonDict.updateBar(Candle)
        if self.ammonDict.inited:
            print(self.ammonDict.DataFrame())
        self.writeCtaLog('on----------MMMMMMMMMMMMMMMMMMM------------Bar: %s '%Candle.datetime)

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        pass
    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送（必须由用户继承实现）"""
        pass
    #----------------------------------------------------------------------
    def onStopOrder(self, so):
        """停止单推送"""
        pass